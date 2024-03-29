from across_client.base.plan import PlanBase
from across_client.base.schema import PlanGetSchema
from .constants import MISSION
from .schema import (
    SwiftPlanEntry,
    SwiftPlanPutSchema,
    SwiftPlanSchema,
)


class SwiftPlan(PlanBase):
    """
    SwiftPlan class represents a plan for the Swift mission.
    """

    # API definitions
    _mission = MISSION
    _schema = SwiftPlanSchema
    _put_schema = SwiftPlanPutSchema
    _get_schema = PlanGetSchema
    _api_name = "Plan"


# Alias
Plan = SwiftPlan
PlanEntry = SwiftPlanEntry
