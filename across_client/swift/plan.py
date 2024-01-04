from datetime import datetime

from ..across.resolve import ACROSSResolveName
from ..base.common import ACROSSBase
from ..base.coords import ACROSSSkyCoord
from ..base.daterange import ACROSSDateRange
from ..base.user import ACROSSUser
from .constants import MISSION
from .schema import (
    SwiftPlanEntry,
    SwiftPlanGetSchema,
    SwiftPlanPutSchema,
    SwiftPlanSchema,
)


class SwiftPlan(
    ACROSSBase, ACROSSUser, ACROSSResolveName, ACROSSDateRange, ACROSSSkyCoord
):
    """
    SwiftPlan class represents a plan for the Swift mission.

    Parameters
    ----------
    ra : float
        Right Ascension value.
    dec : float
        Declination value.
    begin : datetime
        Start datetime of the plan.
    end : datetime
        End datetime of the plan.
    entries : list
        List of entries.

    Attributes
    ----------
    _mission : str
        Mission name.
    _schema : Schema
        Schema for the plan.
    _put_schema : Schema
        Schema for PUT requests.
    _get_schema : Schema
        Schema for GET requests.
    _api_name : str
        Name of the API.

    Methods
    -------
    """

    # Type hints
    ra: float
    dec: float
    begin: datetime
    end: datetime
    entries: list

    # API definitions
    _mission = MISSION
    _schema = SwiftPlanSchema
    _put_schema = SwiftPlanPutSchema
    _get_schema = SwiftPlanGetSchema
    _api_name = "Plan"

    def __init__(self, **kwargs):
        self.entries = []
        for k, a in kwargs.items():
            setattr(self, k, a)


# Alias
Plan = SwiftPlan
PlanEntry = SwiftPlanEntry
