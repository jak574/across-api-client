from datetime import datetime
from across_client.swift.schema import SwiftObservationsGetSchema, SwiftObservationsPutSchema, SwiftObservationsSchema
from ..base import ACROSSBase
from ..daterange import ACROSSDateRange
from ..schema import JobStatus
from ..resolve import ACROSSResolveName
from ..user import ACROSSUser
from .constants import MISSION


class SwiftObservations(ACROSSBase, ACROSSUser, ACROSSResolveName, ACROSSDateRange):
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
    _put_schema = SwiftObservationsPutSchema
    _get_schema = SwiftObservationsGetSchema
    _api_name = "Observations"

    def __init__(self, **kwargs):
        self.status = JobStatus()
        self.entries = []
        [setattr(self, k, a) for k, a in kwargs.items()]


# Alias
Observations = SwiftObservations
