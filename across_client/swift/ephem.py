from datetime import datetime

from ..across.resolve import ACROSSResolveName
from ..base.common import ACROSSBase
from ..base.daterange import ACROSSDateRange
from ..base.schema import JobInfo, EphemGetSchema, EphemSchema, VisWindow
from .constants import MISSION


class SwiftEphem(ACROSSBase, ACROSSResolveName, ACROSSDateRange):
    """
    SwiftEphem class for handling Swift ephemeris data.

    Parameters:
    ----------
    begin : datetime
        Start date and time.
    end : datetime
        End date and time.
    stepsize : int
        Step size in seconds.

    Attributes:
    ----------
    _mission : str
        Mission name.
    _api_name : str
        API name.
    _schema : str
        Schema name.
    _get_schema : str
        Get schema name.
    status : JobInfo
        Job information.

    Methods:
    -------
    __init__(self, **kwargs)
        Initializes a new instance of the SwiftEphem class.

    """

    # Type hints
    ra: float
    dec: float
    begin: datetime
    end: datetime
    hires: bool = True
    entries: list

    # API definitions
    _mission = MISSION
    _api_name = "Ephem"
    _schema = EphemSchema
    _get_schema = EphemGetSchema

    def __init__(self, **kwargs):
        self.status = JobInfo()
        for k, a in kwargs.items():
            setattr(self, k, a)


# Alias
Ephem = SwiftEphem
SwiftVisWindow = VisWindow