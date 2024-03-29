from dataclasses import dataclass
from typing import Optional


@dataclass
class ACROSSUser:
    """
    Represents an ACROSS user.

    Attributes
    ----------
    username : Optional[str]
        The username of the user.
    api_key : Optional[str]
        The API key associated with the user.

    """

    username: Optional[str] = None
    api_key: Optional[str] = None
