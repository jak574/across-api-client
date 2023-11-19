from datetime import datetime, timedelta
from typing import Optional, Union

from ..functions import convert_timedelta, convert_to_dt  # type: ignore


class ACROSSDateRange:
    """
    Represents a date range in the ACROSS API.

    Parameters
    ----------
    begin : datetime
        The start date of the range.
    end : Optional[datetime], optional
        The end date of the range.

    Attributes
    ----------
    begin : datetime
        The start date of the range.
    end : Optional[datetime]
        The end date of the range.
    _length : Union[float, timedelta, str, None]
        The length of the date range.

    Properties
    ----------
    length : Union[float, timedelta, str, None]
        The length of the date range.

    Methods
    -------
    None
    """

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
