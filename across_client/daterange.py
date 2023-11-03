from marshmallow import Schema, fields
from typing import Optional, Union
from datetime import datetime, timedelta
from .functions import convert_to_dt, convert_timedelta


class DateTime(fields.DateTime):
    """Version of DateTime that accepts multiple formats"""

    def _serialize(self, value, attr, obj, **kwargs) -> Optional[str]:
        if value is None:
            return None
        return convert_to_dt(value).strftime("%Y-%m-%d %H:%M:%S")


class DateRangeSchema(Schema):
    begin = DateTime(format="%Y-%m-%d %H:%M:%S", required=False, allow_none=True)
    end = DateTime(format="%Y-%m-%d %H:%M:%S", required=False, allow_none=True)


class ACROSSDateRange:
    begin: datetime
    end: Optional[datetime]
    _length: Union[float, timedelta, str, None]

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, td: Union[float, timedelta, str, None]):
        self._length = td
        if hasattr(self, "begin") and self.begin is not None:
            if hasattr(self, "end") is False or self.end is not None:
                self.end = convert_to_dt(self.begin) + convert_timedelta(td)
