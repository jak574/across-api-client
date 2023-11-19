from datetime import datetime

from ..across.resolve import ACROSSResolveName
from ..base.common import ACROSSBase
from ..base.daterange import ACROSSDateRange
from ..base.schema import JobInfo, VisibilityGetSchema, VisibilitySchema
from .constants import MISSION


class BurstCubeVisibility(ACROSSBase, ACROSSResolveName, ACROSSDateRange):
    """
    Class representing the visibility of BurstCube.

    Parameters:
    ----------
    ra : float
        Right Ascension of the target.
    dec : float
        Declination of the target.
    begin : datetime
        Start time of the visibility period.
    end : datetime
        End time of the visibility period.
    hires : bool
        Flag indicating whether high-resolution data is requested.
    entries : list
        List of entries.

    Attributes:
    ----------
    _mission : str
        Mission name.
    _api_name : str
        API name.
    _schema : VisibilitySchema
        Schema for visibility data.
    _get_schema : VisibilityGetSchema
        Schema for getting visibility data.
    status : JobInfo
        Status of the job.

    Methods:
    -------
    __init__(self, **kwargs)
        Initializes a new instance of the BurstCubeVisibility class.
    """

    ra: float
    dec: float
    begin: datetime
    end: datetime
    hires: bool
    entries: list

    _mission = MISSION
    _api_name = "Visibility"
    _schema = VisibilitySchema
    _get_schema = VisibilityGetSchema

    def __init__(self, **kwargs):
        self.status = JobInfo()
        for k, a in kwargs.items():
            setattr(self, k, a)


# Alias
Visibility = BurstCubeVisibility
