from datetime import datetime

from ..across.resolve import ACROSSResolveName
from ..base.common import ACROSSBase
from ..base.daterange import ACROSSDateRange
from ..base.schema import JobStatus
from ..base.user import ACROSSUser
from .constants import MISSION
from .schema import (
    SwiftPlanGetSchema,
    SwiftPlanPutSchema,
    SwiftPlanSchema,
    SwiftPlanEntry,
)


class SwiftPlan(ACROSSBase, ACROSSUser, ACROSSResolveName, ACROSSDateRange):
    # Type hints
    ra: float
    dec: float
    begin: datetime
    end: datetime
    hires: bool
    entries: list

    # API definitions
    _mission = MISSION
    _schema = SwiftPlanSchema
    _put_schema = SwiftPlanPutSchema
    _get_schema = SwiftPlanGetSchema
    _api_name = "Plan"

    def __init__(self, **kwargs):
        self.status = JobStatus()
        self.entries = []
        [setattr(self, k, a) for k, a in kwargs.items()]


# Alias
Plan = SwiftPlan
PlanEntry = SwiftPlanEntry
