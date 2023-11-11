from datetime import datetime
from .schema import (
    BurstCubeTOOGetSchema,
    BurstCubeTOOPostSchema,
    BurstCubeTOOPutSchema,
    BurstCubeTOORequestsGetSchema,
    BurstCubeTOORequestsSchema,
    BurstCubeTOOSchema,
)

from ..base.base import ACROSSBase
from ..base.daterange import ACROSSDateRange
from ..base.schema import JobStatus
from ..across.resolve import ACROSSResolveName
from ..base.user import ACROSSUser
from .constants import MISSION


class TOO(ACROSSBase, ACROSSUser, ACROSSResolveName, ACROSSDateRange):
    trigger_mission: str
    trigger_instrument: str
    trigger_id: str
    trigger_time: datetime
    ra: float
    dec: float
    begin: datetime
    end: datetime
    exposure: float
    offset: float
    status: JobStatus

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
