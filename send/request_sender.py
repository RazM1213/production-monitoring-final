from abc import ABC, abstractmethod
from asyncio import Task
from datetime import datetime


class RequestSender(ABC):
    def __init__(self):
        self.start_time = datetime.now()

    @abstractmethod
    def send_request(self, session) -> Task:
        pass
