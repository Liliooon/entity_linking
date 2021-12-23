import copy
import json
from typing import *

import pymorphy2
import spacy as sp
import wikipediaapi
from transformers import pipeline

import settings


class WikiModel:
    def retrieve(self, ner_model_output: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        raise NotImplementedError()


class NerToHtmlModel:
    def transform(self, text: str, ner_model_output: List[Dict[str, Any]]) -> str:
        raise NotImplementedError()


class NerModel:
    def process(self, text: str) -> List[Dict[str, Any]]:
        raise NotImplementedError()


class TransformersNerModel(NerModel):
    fixed_punctuation = "!\"#$%&'()*+,./:;<=>?@[\\]^_`{|}~"

    def __init__(self):
        super(TransformersNerModel, self).__init__()
        self.pipeline = pipeline(
            "token-classification",
            model=settings.ner_model_id,
            aggregation_strategy="simple",
        )

    def __postprocess(
        self, pipeline_output: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        output = copy.deepcopy(pipeline_output)
        starts_map = {v["start"]: {"idx": i, "item": v} for i, v in enumerate(output)}
        folded_results = list()
        already_folded = set()
        for i, item in enumerate(output):
            if i not in already_folded:
                if item["end"] in starts_map:
                    to_fold_item = starts_map[item["end"]]["item"]
                    to_fold_idx = starts_map[item["end"]]["idx"]
                    item["end"] = to_fold_item["end"]
                    item["word"] += to_fold_item["word"]
                    item["score"] = (item["score"] + to_fold_item["score"]) / 2

                    already_folded.add(to_fold_idx)

                item["word"] = item["word"].translate(
                    str.maketrans("", "", self.fixed_punctuation)
                )
                item["score"] = float(item["score"])
                folded_results.append(item)

        return folded_results

    def process(self, text: str) -> List[Dict[str, Any]]:
        pipeline_output = self.pipeline(text)
        processed = self.__postprocess(pipeline_output)
        return processed


class SpacyNerToHtmlModel(NerToHtmlModel):
    def __init__(self):
        super(SpacyNerToHtmlModel, self).__init__()
        self.options = settings.spacy_colors

    @staticmethod
    def convert_to_spacy_format(text, result):
        output = {"text": text, "title": None}
        ents = []
        for res in result:
            ents.append(
                {"start": res["start"], "end": res["end"], "label": res["entity_group"]}
            )

        output["ents"] = ents
        return output

    def generate_html(self, ner_data: Dict[str, Any]) -> str:
        html = sp.displacy.render(
            ner_data, style="ent", options=self.options, manual=True, jupyter=False
        )
        return html

    def transform(self, text: str, ner_model_output: List[Dict[str, Any]]) -> str:
        ner_data = self.convert_to_spacy_format(text, ner_model_output)
        html = self.generate_html(ner_data)
        return html


class ApiClientWikiModel(WikiModel):
    def __init__(self):
        super(ApiClientWikiModel, self).__init__()
        self.wiki_api_client = wikipediaapi.Wikipedia(settings.wiki_language)
        self.morph = pymorphy2.MorphAnalyzer(lang=settings.wiki_language)

    def __get_info(self, entity):
        page_py = self.wiki_api_client.page("{}".format(entity))
        if page_py.exists():
            info = [page_py.summary, page_py.canonicalurl]
            return info
        else:
            entity = " ".join(
                [
                    self.morph.parse(ent)[0].inflect({"nomn"})[0]
                    for ent in entity.split()
                ]
            ).title()
            page_py = self.wiki_api_client.page("{}".format(entity))
            if page_py.exists():
                info = [page_py.summary, page_py.canonicalurl]
                return info
            else:
                info = [0, 1]
                return info

    def retrieve(self, ner_model_output: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for i, entity in enumerate(ner_model_output):
            ner_model_output[i]["id"] = i
            info = self.__get_info(ner_model_output[i]["word"])
            ner_model_output[i]["description"] = info[0]
            ner_model_output[i]["link"] = info[1]

        return ner_model_output
