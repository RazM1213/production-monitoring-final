from dataclasses import dataclass


@dataclass
class RequestTime:
    average: int = 0
    maximum: int = 0
    minimum: int = 0
