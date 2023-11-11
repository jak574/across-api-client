from datetime import datetime
from ..base.base import ACROSSBase
from ..base.daterange import ACROSSDateRange
from ..base.schema import JobStatus, VisibilitySchema, VisibilityGetSchema
from ..across.resolve import ACROSSResolveName
from .constants import MISSION


class BurstCubeVisibility(ACROSSBase, ACROSSResolveName, ACROSSDateRange):
    # Type hints
    ra: float
    dec: float
    begin: datetime
    end: datetime
    hires: bool
    entries: list

    # API definitions
    _mission = MISSION
    _api_name = "Visibility"
    _schema = VisibilitySchema
    _get_schema = VisibilityGetSchema

    def __init__(self, **kwargs):
        self.status = JobStatus()
        [setattr(self, k, a) for k, a in kwargs.items()]


# Alias
Visibility = BurstCubeVisibility
