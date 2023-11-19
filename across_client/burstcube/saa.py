from datetime import datetime

from ..across.resolve import ACROSSResolveName
from ..base.common import ACROSSBase
from ..base.daterange import ACROSSDateRange
from ..base.schema import JobInfo, SAAGetSchema, SAASchema, VisWindow
from .constants import MISSION


class BurstCubeSAA(ACROSSBase, ACROSSResolveName, ACROSSDateRange):
    """
    BurstCubeSAA class for handling BurstCube SAA (South Atlantic Anomaly) data.

    Parameters:
    ----------
    ra : float
        Right Ascension value.
    dec : float
        Declination value.
    begin : datetime
        Start date and time.
    end : datetime
        End date and time.
    hires : bool, optional
        Flag indicating whether to use high-resolution data. Default is True.
    entries : list
        List of entries.

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
        Initializes a new instance of the BurstCubeSAA class.

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
    _api_name = "SAA"
    _schema = SAASchema
    _get_schema = SAAGetSchema

    def __init__(self, **kwargs):
        self.status = JobInfo()
        for k, a in kwargs.items():
            setattr(self, k, a)


# Alias
SAA = BurstCubeSAA
BurstCubeVisWindow = VisWindow
