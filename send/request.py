from dataclasses import dataclass
from typing import List, Dict

from utils.http_methods.http_methods_enum import HttpMethodsEnum


@dataclass
class Request:
    request_method: HttpMethodsEnum
    url: str
    status_codes: List[int]
    request_body: Dict = None
    request_headers: Dict = None
    amount: int = 1
