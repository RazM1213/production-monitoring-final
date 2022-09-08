import asyncio

import pytest

from consts.status_codes import ALL_STATUS_CODES
from monitor import Monitor
from send.request import Request
from utils.http_methods.http_methods_enum import HttpMethodsEnum


@pytest.mark.asyncio
def test_valid_send_requests_async_responses_count(loop: asyncio.AbstractEventLoop, monitor: Monitor):
    # Arrange & Act
    responses = loop.run_until_complete(monitor.send_requests_async(list(monitor.requests.keys())[0]))

    # Assert
    assert len(responses) == 10


@pytest.mark.asyncio
def test_valid_send_requests_async_responses_type(loop: asyncio.AbstractEventLoop, monitor: Monitor):
    # Arrange & Act
    responses = loop.run_until_complete(monitor.send_requests_async(list(monitor.requests.keys())[0]))

    # Assert
    for response in responses:
        assert response.method == list(monitor.requests.values())[0].request_method.name
        assert str(response.url) == list(monitor.requests.values())[0].url
        assert response.status == 200


@pytest.mark.asyncio
def test_valid_get_contents_when_available(loop: asyncio.AbstractEventLoop, monitor: Monitor):
    # Arrange
    monitor.requests = {
        "test_route_1": Request(
            request_method=HttpMethodsEnum.GET,
            url="https://petstore.swagger.io/v2/pet/322717570?ID=1",
            status_codes=ALL_STATUS_CODES,
            amount=5
        )
    }
    responses = loop.run_until_complete(monitor.send_requests_async(list(monitor.requests.keys())[0]))

    # Act
    monitor.get_contents(responses)

    # Assert
    assert len(monitor.contents) == list(monitor.requests.values())[0].amount
    for content in monitor.contents:
        assert content == {'code': 1, 'type': 'error', 'message': 'Pet not found'}


@pytest.mark.asyncio
def test_valid_get_contents_when_not_available(loop: asyncio.AbstractEventLoop, monitor: Monitor):
    # Arrange
    responses = loop.run_until_complete(monitor.send_requests_async(list(monitor.requests.keys())[0]))

    # Act
    monitor.get_contents(responses)

    # Assert
    assert monitor.contents == []


@pytest.mark.asyncio
def test_valid_get_responses_values_without_content(loop: asyncio.AbstractEventLoop, monitor: Monitor):
    # Arrange
    responses = loop.run_until_complete(monitor.send_requests_async(list(monitor.requests.keys())[0]))

    # Act
    responses_values = monitor.get_responses_values(responses)

    # Assert
    index = 0
    for response_values in responses_values:
        assert response_values.status_code == responses[index].status
        assert response_values.error_content is None


@pytest.mark.asyncio
def test_valid_get_responses_values_with_content(loop: asyncio.AbstractEventLoop, monitor: Monitor):
    # Arrange
    monitor.requests = {
        "test_route_1": Request(
            request_method=HttpMethodsEnum.GET,
            url="https://petstore.swagger.io/v2/pet/322717570?ID=1",
            status_codes=ALL_STATUS_CODES,
            amount=5
        )
    }
    responses = loop.run_until_complete(monitor.send_requests_async(list(monitor.requests.keys())[0]))

    # Act
    responses_values = monitor.get_responses_values(responses)

    # Assert
    index = 0
    for response_values in responses_values:
        assert response_values.status_code == responses[index].status
        assert response_values.error_content == {'code': 1, 'type': 'error', 'message': 'Pet not found'}
