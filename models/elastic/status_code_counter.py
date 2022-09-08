from dataclasses import dataclass


@dataclass
class StatusCodeCounter:
    status_code: int
    count: int
