from datetime import datetime

from ..across.resolve import ACROSSResolveName
from ..base.common import ACROSSBase
from ..base.daterange import ACROSSDateRange
from ..base.schema import JobStatus
from ..base.user import ACROSSUser
from .constants import MISSION
from .schema import (
    SwiftObservationsGetSchema,
    SwiftObservationsPutSchema,
    SwiftObservationsSchema,
    SwiftObsEntry,
)


class SwiftObservations(ACROSSBase, ACROSSUser, ACROSSResolveName, ACROSSDateRange):
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
        self.status = JobStatus()
        self.entries = []
        [setattr(self, k, a) for k, a in kwargs.items()]


# Alias
Observations = SwiftObservations
ObsEntry = SwiftObsEntry
