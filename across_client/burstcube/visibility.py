from datetime import datetime

from marshmallow import Schema, fields, post_load

from ..base import ACROSSBase
from ..daterange import ACROSSDateRange
from ..jobstatus import JobStatus, JobStatusSchema
from ..resolve import ACROSSResolveName
from ..user import ACROSSUser
from ..visibility import VisibilityArgSchema, VisWindowSchema
from .constants import MISSION


class VisibilitySchema(Schema):
    entries = fields.List(cls_or_instance=fields.Nested(VisWindowSchema))
    status = fields.Nested(JobStatusSchema)

    @post_load
    def make_visibility(self, data, **kwargs):
        return Visibility(**data)


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
    _schema = VisibilitySchema()
    _get_schema = VisibilityArgSchema()

    def __init__(self, **kwargs):
        self.status = JobStatus()
        [setattr(self, k, a) for k, a in kwargs.items()]
