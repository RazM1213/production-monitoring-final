import asyncio

import pytest

from config.config import ROUTE_1, BASE_URL
from consts.status_codes import ALL_STATUS_CODES
from monitor import Monitor
from publish.kafka.kafka_publisher import KafkaPublisher
from send.request import Request
from utils.http_methods.http_methods_enum import HttpMethodsEnum


@pytest.mark.usefixtures("loop", "monitor")
class PytestConfig:
    REQUESTS = {
        "test_route_1": Request(
            request_method=HttpMethodsEnum.GET,
            url=BASE_URL + ROUTE_1,
            status_codes=ALL_STATUS_CODES,
            amount=10
        )
    }

    BOOTSTRAP_SERVERS = ["localhost:9092"]
    TOPIC = "PMTestTopic"
    PUBLISHER = KafkaPublisher(bootstrap_servers=BOOTSTRAP_SERVERS, topic=TOPIC)


@pytest.fixture
def loop():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def monitor():
    monitor = Monitor(requests=PytestConfig.REQUESTS, publisher=PytestConfig.PUBLISHER)
    return monitor

