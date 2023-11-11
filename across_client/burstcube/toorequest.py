from datetime import datetime

from across_client.burstcube.schema import (
    BurstCubeTOOGetSchema,
    BurstCubeTOOPostSchema,
    BurstCubeTOOPutSchema,
    BurstCubeTOORequestsGetSchema,
    BurstCubeTOORequestsSchema,
    BurstCubeTOOSchema,
)

from ..base import ACROSSBase
from ..daterange import ACROSSDateRange, DateTime
from ..schema import JobStatus
from ..resolve import ACROSSResolveName
from ..user import ACROSSUser, UserArgSchema
from .constants import MISSION


class TOO(ACROSSBase, ACROSSUser, ACROSSResolveName, ACROSSDateRange):
    trigger_mission: str
    trigger_instrument: str
    trigger_id: str
    trigger_time: datetime
    ra: float
    dec: float
    begin: float
    end: float
    exposure: float
    offset: float

    # API definitions

    _mission = MISSION
    _api_name = "TOO"
    _schema = BurstCubeTOOSchema
    _put_schema = BurstCubeTOOPutSchema
    _post_schema = BurstCubeTOOPostSchema
    _get_schema = BurstCubeTOOGetSchema

    def __init__(self, **kwargs):
        self.status = JobStatus()
        [setattr(self, k, a) for k, a in kwargs.items()]


class TOORequests(ACROSSBase, ACROSSUser):
    begin: datetime
    end: datetime
    limit: int
    trigger_time: datetime
    entries: list
    status: JobStatus

    _mission = MISSION
    _api_name = "TOORequests"
    _schema = BurstCubeTOORequestsSchema
    _get_schema = BurstCubeTOORequestsGetSchema

    def __init__(self, **kwargs):
        self.status = JobStatus()
        self.entries = []
        [setattr(self, k, a) for k, a in kwargs.items()]
