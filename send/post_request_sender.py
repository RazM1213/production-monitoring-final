import asyncio
from asyncio import Task

from aiohttp import ClientSession

from send.request import Request
from send.request_sender import RequestSender


class PostRequestSender(RequestSender):
    def __init__(self, request: Request):
        super().__init__()
        self.request = request

    def send_request(self, session: ClientSession) -> Task:
        task = asyncio.create_task(session.post(url=self.request.url, headers=self.request.request_headers, json=self.request.request_body, ssl=False))
        return task
