import base64 as b64
import requests
import uuid
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
        api_req = {
            "method": settings.api_method_name,
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "params": {
                "text": text,
                "return_html": True,
                "return_wiki_entities": True
            }
        }
        req = requests.post(self.endpoint, json=api_req)
        logging.info(f"api response: {req.status_code} - {req}")
        if req.status_code == 200:
            response = req.json()
            result = response['result']
            result['html'] = b64.b64decode(result['html']).decode(encoding='utf-8')
            result['entities'] = list(filter(lambda x: x['description'] != 0, result['entities']))
            return result
        else:
            logging.error(f"Failed communicating with api - {req}")
            return None
