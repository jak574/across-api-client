from datetime import datetime

from ..across.resolve import ACROSSResolveName
from ..base.common import ACROSSBase
from ..base.daterange import ACROSSDateRange
from ..base.schema import JobInfo, VisibilityGetSchema, VisibilitySchema
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
        self.status = JobInfo()
        [setattr(self, k, a) for k, a in kwargs.items()]


# Alias
Visibility = BurstCubeVisibility
