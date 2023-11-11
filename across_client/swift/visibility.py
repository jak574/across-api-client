from datetime import datetime
from ..base import ACROSSBase
from ..daterange import ACROSSDateRange
from ..schema import JobStatus, VisibilitySchema, VisibilityGetSchema
from ..resolve import ACROSSResolveName
from ..user import ACROSSUser
from ..visibility import VisibilityArgSchema, VisWindowSchema
from .constants import MISSION


class Visibility(ACROSSBase, ACROSSUser, ACROSSResolveName, ACROSSDateRange):
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
