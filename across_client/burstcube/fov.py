from datetime import datetime

from ..across.resolve import ACROSSResolveName
from ..base.common import ACROSSBase
from ..base.daterange import ACROSSDateRange
from ..base.schema import JobInfo
from .constants import MISSION
from .schema import BurstCubeFOVCheckGetSchema, BurstCubeFOVCheckSchema


class BurstCubeFOVCheck(ACROSSBase, ACROSSResolveName, ACROSSDateRange):
    """
    Class representing a BurstCube FOV Check.

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
    _schema = BurstCubeFOVCheckSchema
    _get_schema = BurstCubeFOVCheckGetSchema
    _api_name = "FOVCheck"

    def __init__(self, **kwargs):
        self.status = JobInfo()
        self.entries = []
        for k, a in kwargs.items():
            setattr(self, k, a)


# Alias
FOVCheck = BurstCubeFOVCheck
