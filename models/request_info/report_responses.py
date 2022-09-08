from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict


@dataclass
class ErrorRequest:
    position: int
    content: str


@dataclass
class ReportResponses:
    request_amount: int
    status_codes: Dict[int, int] = field(default_factory=lambda: {})
    error_requests_info: Dict[int, List[ErrorRequest]] = field(default_factory=lambda: {})
    is_failed: bool = False
    error_count: int = 0
    # time: datetime = datetime.now()
    request_times: List[int] = field(default_factory=lambda: [])
