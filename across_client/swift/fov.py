from datetime import datetime

from ..across.resolve import ACROSSResolveName
from ..base.common import ACROSSBase
from ..base.coords import ACROSSSkyCoord
from ..base.daterange import ACROSSDateRange
from .constants import MISSION
from .schema import SwiftFOVCheckGetSchema, SwiftFOVCheckSchema


class SwiftFOVCheck(ACROSSBase, ACROSSResolveName, ACROSSDateRange, ACROSSSkyCoord):
    """
    Class representing a Swift FOV Check.

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
    _mission = MISSION
    _schema = SwiftFOVCheckSchema
    _get_schema = SwiftFOVCheckGetSchema
    _api_name = "FOVCheck"

    def __init__(self, **kwargs):
        self.entries = []
        for k, a in kwargs.items():
            setattr(self, k, a)
        # As this is a GET only class, we can validate and get the data
        if self.validate_get():
            self.get()


# Alias
FOVCheck = SwiftFOVCheck
