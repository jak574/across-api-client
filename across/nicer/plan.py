from ..base import ACROSSBase
from ..coords import CoordSchema
from ..user import UserArgSchema

# from ..daterange import DateRangeSchema, ACROSSDateRange
from ..jobstatus import JobStatus, JobStatusSchema
from marshmallow import fields, post_load, Schema
from dataclasses import dataclass, field, InitVar
from ..functions import convert_timedelta, convert_to_dt
from datetime import datetime
from typing import Optional
from ..daterange import DateTime


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


class PlanArgSchema(UserArgSchema, CoordSchema):
    begin = DateTime(allow_none=True)
    end = DateTime(allow_none=True)
    radius = fields.Float(allow_none=True)
    obsid = fields.Int(allow_none=True)
    targetid = fields.Int(allow_none=True)


class PlanSchema(Schema):
    entries = fields.List(
        cls_or_instance=fields.Nested(PlanEntrySchema), required=False, allow_none=True
    )
    status = fields.Nested(JobStatusSchema)

    @post_load
    def create_planentry(self, data, **kwargs):
        return Plan(**data)


@dataclass
class Plan(ACROSSBase):
    length: InitVar[Optional[float]] = None
    begin: Optional[datetime] = None
    end: Optional[datetime] = None
    ra: Optional[float] = None
    dec: Optional[float] = None
    radius: Optional[float] = None
    obsid: Optional[int] = None
    targetid: Optional[int] = None
    entries: list[PlanEntry] = field(default_factory=list)

    _schema = PlanSchema()
    _arg_schema = PlanArgSchema()
    _mission = "NICER"
    _api_name = "Plan"

    # JobStatus
    status: JobStatus = JobStatus()

    def __post_init__(self, length):
        if self.begin is not None and length is not None:
            self.end = convert_to_dt(self.begin) + convert_timedelta(length)
