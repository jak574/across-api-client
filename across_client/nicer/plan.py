from datetime import datetime

from ..across.resolve import ACROSSResolveName
from ..base.common import ACROSSBase
from ..base.daterange import ACROSSDateRange
from ..base.schema import JobStatus
from ..base.user import ACROSSUser
from .constants import MISSION
from .schema import (
    NICERPlanGetSchema,
    NICERPlanPutSchema,
    NICERPlanSchema,
    NICERPlanEntry,
)


class NICERPlan(ACROSSBase, ACROSSUser, ACROSSResolveName, ACROSSDateRange):
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
        self.status = JobStatus()
        self.entries = []
        [setattr(self, k, a) for k, a in kwargs.items()]


# Alias
Plan = NICERPlan
PlanEntry = NICERPlanEntry
