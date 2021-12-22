from model import TransformersNerModel, SpacyNerToHtmlModel
from typing import *
import base64 as b64

class EntityLinkingController:

    def __init__(self):
        self.ner = TransformersNerModel()
        self.to_html = SpacyNerToHtmlModel()
        # self.wiki_entities = wiki model

    def get_entities(self, text: str, return_html: bool, return_wiki_entities: bool) -> Dict[str, Any]:
        result = {}
        ner = self.ner.process(text)
        result['ner'] = ner
        if return_html:
            html = self.to_html.transform(text, ner)
            html = b64.b64encode(html.encode(encoding='utf-8')).decode(encoding='ascii')
            result['html'] = html
        if return_wiki_entities:
            pass

        return result
