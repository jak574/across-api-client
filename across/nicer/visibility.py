from datetime import datetime
from ..base import ACROSSBase
from ..user import ACROSSUser
from ..jobstatus import JobStatus, JobStatusSchema
from ..daterange import ACROSSDateRange
from marshmallow import Schema, fields, post_load
from ..visibility import (
    VisWindowSchema as VWSchema,
    VisibilityArgSchema,
    VisWindow as VW,
)
from .constants import MISSION
from ..resolve import ACROSSResolveName
from dataclasses import dataclass


class VisWindowSchema(VWSchema):
    initial = fields.Str()
    final = fields.Str()

    @post_load
    def make_viswindow(self, data, **kwargs):
        return VisWindow(**data)


@dataclass
class VisWindow(VW):
    _schema = VisWindowSchema()
    _arg_schema = VisWindowSchema()
    begin: datetime
    end: datetime
    initial: str
    final: str

    @property
    def _table(self):
        header = ["begin", "end", "initial", "final"]
        return header, [[self.begin, self.end, self.initial, self.final]]


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
