from datetime import datetime
from typing import Any

from ..across.resolve import ACROSSResolveName
from ..base.common import ACROSSBase
from ..base.coords import ACROSSSkyCoord
from ..base.daterange import ACROSSDateRange


class FOVCheckBase(ACROSSBase, ACROSSResolveName, ACROSSDateRange, ACROSSSkyCoord):
    """
    Class representing a  FOV Check.

    Parameters:
    ----------
    ra : float
        Right Ascension coordinate.
    dec : float
        Declination coordinate.
    begin : datetime
        Start date and time of the observation.
    end : datetime
        End date and time of the observation.
    """

    # Type hints
    ra: float
    dec: float
    begin: datetime
    end: datetime

    # API definitions
    _mission: str
    _schema: Any
    _get_schema: Any
    _api_name = "FOVCheck"

    def __init__(self, **kwargs):
        self.entries = []
        for k, a in kwargs.items():
            setattr(self, k, a)
        # As this is a GET only class, we can validate and get the data
        if self.validate_get():
            self.get()
