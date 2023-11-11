from dataclasses import dataclass
from typing import Optional


@dataclass
class ACROSSUser:
    username: Optional[str] = None
    api_key: Optional[str] = None
