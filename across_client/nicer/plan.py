from datetime import datetime
from .schema import NICERPlanGetSchema, NICERPlanSchema
from ..base import ACROSSBase
from ..schema import CoordSchema
from ..daterange import ACROSSDateRange
from ..schema import JobStatus, PlanGetSchemaBase, PlanSchemaBase, PlanEntryBase
from ..resolve import ACROSSResolveName
from ..user import ACROSSUser, UserArgSchema
from .constants import MISSION


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
    _put_schema = NICERPlanGetSchema
    _get_schema = NICERPlanGetSchema
    _api_name = "Plan"

    def __init__(self, **kwargs):
        self.status = JobStatus()
        self.entries = []
        [setattr(self, k, a) for k, a in kwargs.items()]

# Alias
Plan = NICERPlan