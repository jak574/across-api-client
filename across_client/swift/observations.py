from datetime import datetime

from ..across.resolve import ACROSSResolveName
from ..base.common import ACROSSBase
from ..base.coords import ACROSSSkyCoord
from ..base.daterange import ACROSSDateRange
from ..base.schema import JobInfo
from ..base.user import ACROSSUser
from .constants import MISSION
from .schema import (
    SwiftObsEntry,
    SwiftObservationsGetSchema,
    SwiftObservationsPutSchema,
    SwiftObservationsSchema,
)


class SwiftObservations(
    ACROSSBase, ACROSSUser, ACROSSResolveName, ACROSSDateRange, ACROSSSkyCoord
):
    """
    Class representing Swift observations.

    Parameters:
    ----------
    ra : float
        Right Ascension of the observation.
    dec : float
        Declination of the observation.
    begin : datetime
        Start time of the observation.
    end : datetime
        End time of the observation.
    entries : list
        List of observation entries.

    Attributes:
    ----------
    _mission : str
        Mission name.
    _schema : SwiftObservationsSchema
        Schema for Swift observations.
    _put_schema : SwiftObservationsPutSchema
        Schema for putting Swift observations.
    _get_schema : SwiftObservationsGetSchema
        Schema for getting Swift observations.
    _api_name : str
        Name of the API.

    Methods:
    -------
    __init__(self, **kwargs)
        Initializes a new instance of the SwiftObservations class.
    """

    # Type hints
    ra: float
    dec: float
    begin: datetime
    end: datetime
    entries: list

    # API definitions
    _mission = MISSION
    _schema = SwiftObservationsSchema
    _put_schema = SwiftObservationsPutSchema
    _get_schema = SwiftObservationsGetSchema
    _api_name = "Observations"

    def __init__(self, **kwargs):
        self.entries = []
        for k, a in kwargs.items():
            setattr(self, k, a)


# Alias
Observations = SwiftObservations
ObsEntry = SwiftObsEntry
