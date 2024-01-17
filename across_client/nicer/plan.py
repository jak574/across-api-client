from across_client.base.plan import PlanBase
from across_client.base.schema import PlanGetSchema
from .constants import MISSION
from .schema import (
    NICERPlanEntry,
    NICERPlanPutSchema,
    NICERPlanSchema,
)


class NICERPlan(PlanBase):
    """
    NICERPlan class represents a plan for the NICER mission.
    """

    # API definitions
    _mission = MISSION
    _schema = NICERPlanSchema
    _put_schema = NICERPlanPutSchema
    _get_schema = PlanGetSchema
    _api_name = "Plan"


# Alias
Plan = NICERPlan
PlanEntry = NICERPlanEntry
