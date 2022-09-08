import datetime
from dataclasses import dataclass


@dataclass
class ResponseValues:
    time: datetime.timedelta
    status_code: int = None
    error_content: str = None
