import base64 as b64
from typing import *

from model import ApiClientWikiModel, SpacyNerToHtmlModel, TransformersNerModel


class EntityLinkingController:
    def __init__(self):
        self.ner = TransformersNerModel()
        self.to_html = SpacyNerToHtmlModel()
        self.wiki_entities = ApiClientWikiModel()

    def get_entities(
        self, text: str, return_html: bool, return_wiki_entities: bool
    ) -> Dict[str, Any]:
        result = {}
        ner = self.ner.process(text)
        if return_html:
            html = self.to_html.transform(text, ner)
            html = b64.b64encode(html.encode(encoding="utf-8")).decode(encoding="ascii")
            result["html"] = html
        if return_wiki_entities:
            result["entities"] = self.wiki_entities.retrieve(ner)
        else:
            result["entities"] = ner

        return result
