from across.base import ACROSSBase
from across.coords import CoordSchema
from across.user import UserArgSchema
from across.daterange import DateRangeSchema, ACROSSDateRange
from across.jobstatus import JobStatus, JobStatusSchema
from marshmallow import fields, post_load, Schema
from dataclasses import dataclass
from datetime import datetime


class PlanEntrySchema(CoordSchema):
    begin = fields.DateTime()
    end = fields.DateTime()
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
    _arg_schema = PlanEntrySchema()
    ra: float
    dec: float
    begin: datetime
    end: datetime
    targname: str
    targetid: int
    obsid: int
    exposure: int
    mode: str


class PlanArgSchema(UserArgSchema, CoordSchema, DateRangeSchema):
    radius = fields.Float()
    obsid = fields.Int()
    targetid = fields.Int()
    # entries = fields.List(
    #     cls_or_instance=fields.Nested(PlanEntrySchema), required=False, allow_none=True
    # )


class PlanSchema(Schema):
    entries = fields.List(
        cls_or_instance=fields.Nested(PlanEntrySchema), required=False, allow_none=True
    )
    status = fields.Nested(JobStatusSchema)

    @post_load
    def create_planentry(self, data, **kwargs):
        return Plan(**data)


class Plan(ACROSSBase, ACROSSDateRange):
    _schema = PlanSchema()
    _arg_schema = PlanArgSchema()
    _mission = "NICER"
    _api_name = "Plan"

    def __init__(self, **kwargs):
        self.entries = []
        self.status = JobStatus()
        [setattr(self, k, a) for k, a in kwargs.items()]
