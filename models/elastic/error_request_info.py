from dataclasses import dataclass
from typing import List


@dataclass
class OrderPositionDetails:
    position: int
    content: str


@dataclass
class ErrorRequestInfo:
    status_code: int
    order_positions: List[OrderPositionDetails]
