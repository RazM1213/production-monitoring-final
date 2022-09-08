import asyncio

from aiohttp import ClientSession

from models.request_info.response_values import ResponseValues
from send.request import Request
from send.request_sender import RequestSender


class GetRequestSender(RequestSender):
    def __init__(self, request: Request):
        super().__init__()
        self.request = request

    def send_request(self, session: ClientSession) -> ResponseValues:
        task = asyncio.create_task(session.get(url=self.request.url, headers=self.request.request_headers, ssl=False))
        return task
