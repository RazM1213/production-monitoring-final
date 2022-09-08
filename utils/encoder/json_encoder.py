import dataclasses
from json import JSONEncoder


class Encoder(JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(0):
            return dataclasses.asdict(o)
        return o.__dict__
