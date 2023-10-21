from dataclasses import dataclass
from typing import Union

@dataclass
class SessionData:
    session_username: str
    api_hash: str
    api_id: int


class PretensionStatus:
    WAIT = 'wait'
    PROCESSING = 'processing'
    CLOSED = 'closed'


@dataclass
class Item:
    width: int
    length: int
    height: int


@dataclass
class Package:
    description: Union[str, None]
    items: list[Item]
