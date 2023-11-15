from datetime import datetime

from ..across.resolve import ACROSSResolveName
from ..base.common import ACROSSBase
from ..base.daterange import ACROSSDateRange
from ..base.schema import JobInfo, SAAGetSchema, SAASchema, VisWindow
from .constants import MISSION


class SwiftSAA(ACROSSBase, ACROSSResolveName, ACROSSDateRange):
    # Type hints
    ra: float
    dec: float
    begin: datetime
    end: datetime
    hires: bool = True
    entries: list

    # API definitions
    _mission = MISSION
    _api_name = "SAA"
    _schema = SAASchema
    _get_schema = SAAGetSchema

    def __init__(self, **kwargs):
        self.status = JobInfo()
        [setattr(self, k, a) for k, a in kwargs.items()]


# Alias
SAA = SwiftSAA
SwiftVisWindow = VisWindow
