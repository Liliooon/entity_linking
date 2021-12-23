import base64 as b64
from jsonrpcclient import request_json, parse_json, Ok
import requests
from typing import *
import settings
import logging

class ApiClient:

    def process_text(self, text: str) -> Union[Dict[str, Any], None]:
        raise NotImplementedError()


class JsonRpcApiClient(ApiClient):

    def __init__(self):
        super(JsonRpcApiClient, self).__init__()
        self.endpoint = settings.api_address

    def process_text(self, text: str) -> Union[Dict[str, Any], None]:
        api_req = request_json(
            settings.api_method_name,
            params={
                "text": text,
                "return_html": True,
                "return_wiki_entities": True
            }
        )
        req = requests.post(self.endpoint, json=api_req)
        logging.info(f"api response: {req.status_code} - {req}")
        response = parse_json(req.json())
        if isinstance(response, Ok):
            result = response.result
            result['html'] = b64.b64decode(result['html']).decode(encoding='utf-8')
            return result
        else:
            logging.error(response.message)
            return None
