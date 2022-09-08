import asyncio
import json
from datetime import datetime
from typing import List, Dict

import aiohttp
from aiohttp import ClientResponse

from consts.formats import ENCODE_FORMAT
from models.request_info.response_values import ResponseValues
from publish.i_publisher import IPublisher
from send.request import Request
from transform.response.response_transformer import ResponseTransformer
from utils.http_methods import http_method_func_mapping


class Monitor:
    def __init__(self, requests: Dict[str, Request], publisher: IPublisher):
        self.requests = requests
        self.response_transformer = ResponseTransformer()
        self.publisher = publisher
        self.start_time = None
        self.contents = []

    async def send_requests_async(self, route_name: str) -> List[ClientResponse]:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for request_index in range(self.requests[route_name].amount):
                sender = http_method_func_mapping.HTTP_METHODS_FUNCS[self.requests[route_name].request_method.value]
                tasks.append(sender(self.requests[route_name], session))
            self.start_time = datetime.now()
            responses = await asyncio.gather(*tasks)

        await self.get_contents(responses)
        return responses

    async def get_contents(self, client_responses: List[ClientResponse]):
        for response in client_responses:
            if not response.status // 100 == 2:
                content = await response.content.read()
                self.contents.append(json.loads(content.decode(ENCODE_FORMAT)))

    def get_responses_values(self, client_responses: List[ClientResponse]) -> List[ResponseValues]:
        responses_values = []
        count = 0
        for client_response in client_responses:
            if client_response.status // 100 == 2:
                responses_values.append(ResponseValues(datetime.now() - self.start_time, client_response.status))
            else:
                responses_values.append(ResponseValues(datetime.now() - self.start_time, client_response.status, self.contents[count]))
            count += 1
        return responses_values

    def start(self):
        for route in self.requests:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            responses = asyncio.run(self.send_requests_async(route))
            responses_values = self.get_responses_values(responses)
            report_responses = self.response_transformer.get_report_responses(responses_values)
            elastic_report_doc = self.response_transformer.get_elastic_report_doc(
                route,
                report_responses
            )
            self.publisher.publish(elastic_report_doc)
