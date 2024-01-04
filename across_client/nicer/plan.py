from across_client.base.plan import PlanBase
from .constants import MISSION
from .schema import (
    NICERPlanEntry,
    NICERPlanGetSchema,
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
    _get_schema = NICERPlanGetSchema
    _api_name = "Plan"


# Alias
Plan = NICERPlan
PlanEntry = NICERPlanEntry
