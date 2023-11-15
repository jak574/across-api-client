from datetime import datetime
from typing import Optional

from ..across.resolve import ACROSSResolveName
from ..base.common import ACROSSBase
from ..base.daterange import ACROSSDateRange
from ..base.schema import JobInfo
from ..base.user import ACROSSUser
from .constants import MISSION
from .schema import (
    BurstCubeTOOGetSchema,
    BurstCubeTOOPostSchema,
    BurstCubeTOOPutSchema,
    BurstCubeTOORequestsGetSchema,
    BurstCubeTOORequestsSchema,
    BurstCubeTOOSchema,
)


class TOO(ACROSSBase, ACROSSUser, ACROSSResolveName, ACROSSDateRange):
    trigger_mission: str
    trigger_instrument: str
    trigger_id: str
    trigger_time: datetime
    ra: Optional[float]
    dec: Optional[float]
    begin: datetime
    end: datetime
    exposure: float
    offset: float
    status: JobInfo

    # API definitions

    _mission = MISSION
    _api_name = "TOO"
    _schema = BurstCubeTOOSchema
    _put_schema = BurstCubeTOOPutSchema
    _post_schema = BurstCubeTOOPostSchema
    _get_schema = BurstCubeTOOGetSchema
    _del_schema = BurstCubeTOOGetSchema

    def __init__(self, **kwargs):
        self.exposure = 200
        self.offset = -50
        self.status = JobInfo()
        [setattr(self, k, a) for k, a in kwargs.items()]


class TOORequests(ACROSSBase, ACROSSUser):
    begin: datetime
    end: datetime
    limit: int
    trigger_time: datetime
    entries: list
    status: JobInfo

    _mission = MISSION
    _api_name = "TOORequests"
    _schema = BurstCubeTOORequestsSchema
    _get_schema = BurstCubeTOORequestsGetSchema

    def __init__(self, **kwargs):
        self.status = JobInfo()
        self.entries = []
        [setattr(self, k, a) for k, a in kwargs.items()]


# Alias
BurstCubeTOO = TOO
