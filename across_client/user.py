from dataclasses import dataclass
from typing import Optional
from marshmallow import Schema, fields, validates_schema, ValidationError


class UserArgSchema(Schema):
    username = fields.Str(allow_none=True)
    api_key = fields.Str(allow_none=True)

    @validates_schema
    def username_requires_api_key(self, data, **kwargs):
        if (
            "username" in data and ("api_key" not in data or data["api_key"] is None)
        ) and (data["username"] != "anonymous" or data["username"] is not None):
            raise ValidationError("api_key required if username is set")


@dataclass
class ACROSSUser:
    username: Optional[str] = None
    api_key: Optional[str] = None
