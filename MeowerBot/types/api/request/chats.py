from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import TypedDict


class ChatBody( TypedDict ):
    nickname: str

