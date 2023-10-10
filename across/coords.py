from marshmallow import Schema, fields, validates_schema, ValidationError
from .resolve import Resolve
from typing import Optional


class CoordSchema(Schema):
    ra = fields.Float()
    dec = fields.Float()
    # poserr = fields.Float(required=False, allow_none=True)

    @validates_schema
    def coord_check(self, data, **kwargs):
        if "ra" in data and "dec" in data:
            if data["ra"] is not None and data["dec"] is not None:
                if (
                    data["ra"] >= 0
                    and data["ra"] <= 360
                    and data["dec"] >= -90
                    and data["dec"] <= 90
                ):
                    pass
                else:
                    raise ValidationError("RA/Dec not in valid range.")
