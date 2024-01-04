from across_client.base.plan import PlanBase
from .constants import MISSION
from .schema import (
    BurstCubePlanEntry,
    BurstCubePlanGetSchema,
    BurstCubePlanPutSchema,
    BurstCubePlanSchema,
)


class BurstCubePlan(PlanBase):
    """
    BurstCubePlan class represents a plan for the BurstCube mission.
    """

    # API definitions
    _mission = MISSION
    _schema = BurstCubePlanSchema
    _put_schema = BurstCubePlanPutSchema
    _get_schema = BurstCubePlanGetSchema
    _api_name = "Plan"


# Alias
Plan = BurstCubePlan
PlanEntry = BurstCubePlanEntry
