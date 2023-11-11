from datetime import datetime

from ..across.resolve import ACROSSResolveName
from ..base.base import ACROSSBase
from ..base.daterange import ACROSSDateRange
from ..base.schema import JobStatus
from .constants import MISSION
from .schema import SwiftObservationsGetSchema, SwiftObservationsSchema


class SwiftObservations(ACROSSBase, ACROSSResolveName, ACROSSDateRange):
    # Type hints
    ra: float
    dec: float
    begin: datetime
    end: datetime
    hires: bool
    entries: list

    # API definitions
    _mission = MISSION
    _schema = SwiftObservationsSchema
    _put_schema = SwiftObservationsGetSchema
    _get_schema = SwiftObservationsGetSchema
    _api_name = "Observations"

    def __init__(self, **kwargs):
        self.status = JobStatus()
        self.entries = []
        [setattr(self, k, a) for k, a in kwargs.items()]


# Alias
Observations = SwiftObservations
