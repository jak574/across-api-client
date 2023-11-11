from datetime import datetime, timedelta
from typing import Optional, Union
from .functions import convert_timedelta, convert_to_dt  # type: ignore


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
