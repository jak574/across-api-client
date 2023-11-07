from ..resolve import ACROSSResolveName
from ..base import ACROSSBase
from ..coords import CoordSchema
from ..user import ACROSSUser, UserArgSchema
from .constants import MISSION
from ..daterange import ACROSSDateRange
from ..jobstatus import JobStatus, JobStatusSchema
from marshmallow import fields, post_load, Schema
from dataclasses import dataclass
from datetime import datetime
from ..daterange import DateTime


class ObsEntrySchema(CoordSchema):
    roll = fields.Float()
    begin = fields.DateTime()
    end = fields.DateTime()
    slew = fields.Int()
    targname = fields.Str()
    targetid = fields.Int()
    segment = fields.Int()
    obsid = fields.Str()
    exposure = fields.Int()
    xrtmode = fields.Int()
    uvotmode = fields.Int()
    batmode = fields.Int()
    merit = fields.Int()

    @post_load
    def create_obsentry(self, data, **kwargs):
        return ObsEntry(**data)


@dataclass
class ObsEntry(ACROSSBase):
    _schema = ObsEntrySchema()
    _get_schema = ObsEntrySchema()
    _put_schema = ObsEntrySchema()
    begin: datetime
    end: datetime
    slew: int
    ra: float
    dec: float
    roll: float
    targname: str
    targetid: int
    segment: int
    obsid: str
    exposure: int
    xrtmode: int
    uvotmode: int
    batmode: int
    merit: int


class ObservationsArgSchema(UserArgSchema, CoordSchema):
    begin = DateTime(allow_none=True)
    end = DateTime(allow_none=True)
    radius = fields.Float(allow_none=True)
    obsid = fields.Int(allow_none=True)
    targetid = fields.Int(allow_none=True)


class ObservationsEntriesSchema(Schema):
    entries = fields.List(
        cls_or_instance=fields.Nested(ObsEntrySchema), required=False, allow_none=True
    )


class ObservationsSchema(ObservationsEntriesSchema):

    status = fields.Nested(JobStatusSchema)

    @post_load
    def create_observations(self, data, **kwargs):
        return Observations(**data)


class Observations(ACROSSBase, ACROSSUser, ACROSSResolveName, ACROSSDateRange):
    # Type hints
    ra: float
    dec: float
    begin: datetime
    end: datetime
    hires: bool
    entries: list

    # API definitions
    _mission = MISSION
    _schema = ObservationsSchema()
    _put_schema = ObservationsEntriesSchema()
    _get_schema = ObservationsArgSchema()
    _api_name = "Observations"

    def __init__(self, **kwargs):
        self.status = JobStatus()
        self.entries = []
        [setattr(self, k, a) for k, a in kwargs.items()]
