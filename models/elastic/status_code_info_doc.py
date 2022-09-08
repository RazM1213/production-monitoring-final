from dataclasses import dataclass
from typing import List

from models.elastic.error_request_info import ErrorRequestInfo
from models.elastic.status_code_counter import StatusCodeCounter


@dataclass
class StatusCodesInfo:
    status_codes_counter: List[StatusCodeCounter]
    error_requests_info: List[ErrorRequestInfo]
    is_failed: bool = False
    error_count: int = 0
