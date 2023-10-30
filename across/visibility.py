from datetime import datetime
from dataclasses import dataclass
from .base import ACROSSBase
from marshmallow import Schema, fields, post_load
from .user import UserArgSchema
from .coords import CoordSchema
from .daterange import DateRangeSchema


class VisWindowSchema(Schema):
    begin = fields.DateTime(format="%Y-%m-%dT%H:%M:%S", required=True)
    end = fields.DateTime(format="%Y-%m-%dT%H:%M:%S", required=True)

    @post_load
    def make_viswindow(self, data, **kwargs):
        return VisWindow(**data)


class VisibilityArgSchema(UserArgSchema, DateRangeSchema, CoordSchema):
    hires = fields.Bool()


@dataclass
class VisWindow(ACROSSBase):
    begin: datetime
    end: datetime
    _schema = VisWindowSchema()
    _get_schema = _schema

    @property
    def exposure(self):
        return self.end - self.begin
