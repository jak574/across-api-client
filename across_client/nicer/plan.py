from dataclasses import dataclass
from datetime import datetime

from marshmallow import Schema, fields, post_load

from ..base import ACROSSBase
from ..coords import CoordSchema
from ..daterange import ACROSSDateRange, DateTime
from ..jobstatus import JobStatus, JobStatusSchema
from ..resolve import ACROSSResolveName
from ..user import ACROSSUser, UserArgSchema
from .constants import MISSION


class PlanEntrySchema(CoordSchema):
    begin = DateTime(allow_none=True)
    end = DateTime(allow_none=True)
    targname = fields.Str()
    targetid = fields.Int()
    obsid = fields.Int()
    exposure = fields.Int()
    mode = fields.Str()

    @post_load
    def create_planentry(self, data, **kwargs):
        return PlanEntry(**data)


@dataclass
class PlanEntry(ACROSSBase):
    _schema = PlanEntrySchema()
    _get_schema = PlanEntrySchema()
    ra: float
    dec: float
    begin: datetime
    end: datetime
    targname: str
    targetid: int
    obsid: int
    exposure: int
    mode: str


class PlanArgSchema(UserArgSchema, CoordSchema):
    begin = DateTime(allow_none=True)
    end = DateTime(allow_none=True)
    radius = fields.Float(allow_none=True)
    obsid = fields.Int(allow_none=True)
    targetid = fields.Int(allow_none=True)


class PlanEntriesSchema(Schema):
    entries = fields.List(
        cls_or_instance=fields.Nested(PlanEntrySchema), required=False, allow_none=True
    )


class PlanSchema(PlanEntriesSchema):

    status = fields.Nested(JobStatusSchema)

    @post_load
    def create_plan(self, data, **kwargs):
        return Plan(**data)


class Plan(ACROSSBase, ACROSSUser, ACROSSResolveName, ACROSSDateRange):
    # Type hints
    ra: float
    dec: float
    begin: datetime
    end: datetime
    hires: bool
    entries: list

    # API definitions
    _mission = MISSION
    _schema = PlanSchema()
    _put_schema = PlanEntriesSchema()
    _get_schema = PlanArgSchema()
    _api_name = "Plan"

    def __init__(self, **kwargs):
        self.status = JobStatus()
        self.entries = []
        [setattr(self, k, a) for k, a in kwargs.items()]
