from datetime import datetime
from ..base import ACROSSBase
from ..user import ACROSSUser
from ..jobstatus import JobStatus, JobStatusSchema
from ..daterange import ACROSSDateRange
from marshmallow import Schema, fields, post_load
from .constants import MISSION
from ..resolve import ACROSSResolveName
from ..user import UserArgSchema
from ..daterange import DateTime
from ..functions import convert_to_dt
from dataclasses import dataclass


class DateTimeSix(fields.DateTime):
    """Version of DateTime field that returns 6 decimal places on the milliseconds"""

    def _serialize(self, value, attr, obj, **kwargs) -> str:
        return convert_to_dt(value).strftime("%Y-%m-%d %H:%M:%S.%f")


class TOOArgSchema(UserArgSchema):
    trigger_mission = fields.Str(required=True)
    trigger_instrument = fields.Str(required=True)
    trigger_id = fields.Str(required=True)
    trigger_time = DateTimeSix(format="%Y-%m-%d %H:%M:%S.%f", required=True)
    ra = fields.Float(allow_none=True, required=False)
    dec = fields.Float(allow_none=True, required=False)
    begin = DateTime(format="%Y-%m-%d %H:%M:%S", allow_none=True, required=False)
    end = DateTime(format="%Y-%m-%d %H:%M:%S", allow_none=True, required=False)
    exposure = fields.Float(allow_none=True, required=False)
    offset = fields.Float(allow_none=True, required=False)


class TOOSchema(Schema):
    """Schema for the response to a TOO request."""

    too_id = fields.Int(allow_none=True)
    timestamp = fields.DateTime(allow_none=True)
    status = fields.Nested(JobStatusSchema)

    @post_load
    def make_too(self, data, **kwargs):
        return TOO(**data)


class TOO(ACROSSBase, ACROSSUser, ACROSSResolveName, ACROSSDateRange):
    trigger_mission: str
    trigger_instrument: str
    trigger_id: str
    trigger_time: datetime
    ra: float
    dec: float
    begin: float
    end: float
    exposure: float
    offset: float

    # API definitions

    _mission = MISSION
    _api_name = "TOO"
    _schema = TOOSchema()
    _arg_schema = TOOArgSchema()

    def __init__(self, **kwargs):
        self.status = JobStatus()
        [setattr(self, k, a) for k, a in kwargs.items()]


class TOOFullSchema(Schema):
    """Schema to retrieve all infomration about a TOO Request"""

    too_id = fields.Int()
    timestamp = fields.DateTime()
    username = fields.Str()
    trigger_mission = fields.Str()
    trigger_instrument = fields.Str()
    trigger_id = fields.Str()
    trigger_time = fields.Str()
    ra = fields.Float(allow_none=True)
    dec = fields.Float(allow_none=True)
    begin = fields.DateTime()
    end = fields.DateTime()
    exposure = fields.Float()
    offset = fields.Float()

    @post_load
    def make_too(self, data, **kwargs):
        return TOO(**data)


class TOORequestsArgSchema(UserArgSchema):
    begin = fields.DateTime(allow_none=True)
    end = fields.DateTime(allow_none=True)
    trigger_time = fields.DateTime(allow_none=True)
    limit = fields.Int(allow_none=True)


class TOORequestsSchema(Schema):
    entries = fields.List(fields.Nested(TOOFullSchema))
    status = fields.Nested(JobStatusSchema)

    @post_load
    def make_toorequests(self, data, **kwargs):
        return TOORequests(**data)


class TOORequests(ACROSSBase, ACROSSUser):
    begin: datetime
    end: datetime
    limit: int
    trigger_time: datetime
    entries: list
    status: JobStatus

    _mission = MISSION
    _api_name = "TOORequests"
    _schema = TOORequestsSchema()
    _arg_schema = TOORequestsArgSchema()

    def __init__(self, **kwargs):
        self.status = JobStatus()
        self.entries = []
        [setattr(self, k, a) for k, a in kwargs.items()]