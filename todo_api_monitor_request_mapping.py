from config.config import BASE_URL, ROUTE_1, ROUTE_2, POST_REQUEST_BODY
from consts.status_codes import ALL_STATUS_CODES
from send.request import Request
from utils.http_methods.http_methods_enum import HttpMethodsEnum

REQUESTS = {
    ROUTE_1: Request(
        request_method=HttpMethodsEnum.GET,
        url=BASE_URL + ROUTE_1,
        status_codes=ALL_STATUS_CODES,
        amount=10
    ),
    f"GET {ROUTE_2}": Request(
        request_method=HttpMethodsEnum.GET,
        url=BASE_URL + ROUTE_2,
        status_codes=ALL_STATUS_CODES,
        amount=5
    ),
    f"POST {ROUTE_2}": Request(
        request_method=HttpMethodsEnum.POST,
        url=BASE_URL + ROUTE_2,
        status_codes=ALL_STATUS_CODES,
        request_body=POST_REQUEST_BODY,
        amount=10
    )
}
