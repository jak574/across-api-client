from datetime import datetime

from ..across.resolve import ACROSSResolveName
from ..base.common import ACROSSBase
from ..base.daterange import ACROSSDateRange
from ..base.schema import JobStatus
from .constants import MISSION
from .schema import (
    SwiftFOVCheckGetSchema,
    SwiftFOVCheckSchema,
)


class SwiftFOVCheck(ACROSSBase, ACROSSResolveName, ACROSSDateRange):
    # Type hints
    ra: float
    dec: float
    begin: datetime
    end: datetime

    # API definitions
    _mission = MISSION
    _schema = SwiftFOVCheckSchema
    _get_schema = SwiftFOVCheckGetSchema
    _api_name = "FOVCheck"

    def __init__(self, **kwargs):
        self.status = JobStatus()
        self.entries = []
        [setattr(self, k, a) for k, a in kwargs.items()]


# Alias
FOVCheck = SwiftFOVCheck
