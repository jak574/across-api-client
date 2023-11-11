from datetime import datetime
from .schema import SwiftPlanGetSchema, SwiftPlanSchema
from ..base import ACROSSBase
from ..schema import CoordSchema
from ..daterange import ACROSSDateRange
from ..schema import JobStatus, PlanGetSchemaBase, PlanSchemaBase, PlanEntryBase
from ..resolve import ACROSSResolveName
from ..user import ACROSSUser, UserArgSchema
from .constants import MISSION


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
    _put_schema = SwiftPlanGetSchema
    _get_schema = SwiftPlanGetSchema
    _api_name = "Plan"

    def __init__(self, **kwargs):
        self.status = JobStatus()
        self.entries = []
        [setattr(self, k, a) for k, a in kwargs.items()]

# Alias
Plan = SwiftPlan