from across_client.base.plan import PlanBase
from across_client.base.schema import PlanGetSchema
from .constants import MISSION
from .schema import (
    NuSTARPlanEntry,
    NuSTARPlanPutSchema,
    NuSTARPlanSchema,
)


class NuSTARPlan(PlanBase):
    """
    NuSTARPlan class represents a plan for the NuSTAR mission.
    """

    # API definitions
    _mission = MISSION
    _schema = NuSTARPlanSchema
    _put_schema = NuSTARPlanPutSchema
    _get_schema = PlanGetSchema
    _api_name = "Plan"


# Alias
Plan = NuSTARPlan
PlanEntry = NuSTARPlanEntry
