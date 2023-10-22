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
class Package:
    description: Union[str, None]
    width: int = 0
    length: int = 0
    height: int = 0
    weight: int = 0
    cost: int = 0
