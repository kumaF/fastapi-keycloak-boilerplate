import sys

sys_socket = sys.modules.pop("socket", None)
sys_ssl = sys.modules.pop("ssl", None)

import grequests

sys.modules["socket"] = sys_socket
sys.modules["ssl"] = sys_ssl

from .utils import validate_batch_responses
from .exceptions import grequest_exception_handler
from .configs import (
    GCF_BASE_URL,
    MEDIA_LIVE_BASE_URL,
    URL_CONFIGS
)


class Retriever:
    def __init__(self) -> None:
        self._reqs: list = []

    async def init_request(self, req_type: str, type: str, payload = None, params = '', headers = ''):
        BASE_URL = None

        if type == 'subtitle':
            BASE_URL = GCF_BASE_URL
        elif type == 'stream':
            BASE_URL = MEDIA_LIVE_BASE_URL


        self._reqs.append({
            'method': URL_CONFIGS.get(req_type).get("method"),
            'url': f'{BASE_URL}{URL_CONFIGS.get(req_type).get("url")}',
            'json': payload,
            'params': params,
            'headers': headers
        })

    async def fetch_rqs(self) -> list:
        rqs = (grequests.request(
            method=req['method'],
            url=req['url'],
            json=req.get('json', None),
            params=req.get('params', ''),
            headers=req.get('headers', '')
            
        ) for req in self._reqs)

        resps = grequests.map(
            rqs, exception_handler=grequest_exception_handler)

        return await validate_batch_responses(resps)