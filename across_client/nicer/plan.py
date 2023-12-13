from datetime import datetime

from ..base.coords import ACROSSSkyCoord
from ..across.resolve import ACROSSResolveName
from ..base.common import ACROSSBase
from ..base.daterange import ACROSSDateRange
from ..base.schema import JobInfo
from ..base.user import ACROSSUser
from .constants import MISSION
from .schema import (
    NICERPlanEntry,
    NICERPlanGetSchema,
    NICERPlanPutSchema,
    NICERPlanSchema,
)


class NICERPlan(ACROSSBase, ACROSSUser, ACROSSResolveName, ACROSSDateRange, ACROSSSkyCoord):
    # Type hints
    ra: float
    dec: float
    begin: datetime
    end: datetime
    hires: bool
    entries: list

    # API definitions
    _mission = MISSION
    _schema = NICERPlanSchema
    _put_schema = NICERPlanPutSchema
    _get_schema = NICERPlanGetSchema
    _api_name = "Plan"

    def __init__(self, **kwargs):
        self.status = JobInfo()
        self.entries = []
        [setattr(self, k, a) for k, a in kwargs.items()]


# Alias
Plan = NICERPlan
PlanEntry = NICERPlanEntry
