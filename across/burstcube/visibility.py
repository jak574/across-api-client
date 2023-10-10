from datetime import datetime
from ..base import ACROSSBase
from ..user import ACROSSUser
from ..jobstatus import JobStatus, JobStatusSchema
from ..daterange import ACROSSDateRange
from marshmallow import Schema, fields, post_load
from ..visibility import VisWindowSchema, VisibilityArgSchema
from .constants import MISSION
from ..resolve import ACROSSResolveName


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
    _arg_schema = VisibilityArgSchema()

    def __init__(self, **kwargs):
        self.status = JobStatus()
        [setattr(self, k, a) for k, a in kwargs.items()]
