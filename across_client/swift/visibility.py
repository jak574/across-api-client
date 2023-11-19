from datetime import datetime

from ..across.resolve import ACROSSResolveName
from ..base.common import ACROSSBase
from ..base.daterange import ACROSSDateRange
from ..base.schema import JobInfo, VisibilityGetSchema, VisibilitySchema, VisWindow
from .constants import MISSION


class SwiftVisibility(ACROSSBase, ACROSSResolveName, ACROSSDateRange):
    """
    Class representing the visibility of Swift objects.

    Parameters:
    ----------
    ra : float
        Right ascension of the object.
    dec : float
        Declination of the object.
    begin : datetime
        Start time of the visibility period.
    end : datetime
        End time of the visibility period.
    hires : bool, optional
        Flag indicating whether high-resolution data is requested. Default is True.
    entries : list
        List of entries.

    Attributes:
    ----------
    _mission : str
        Mission name.
    _api_name : str
        API name.
    _schema : VisibilitySchema
        Schema for visibility.
    _get_schema : VisibilityGetSchema
        Schema for getting visibility.
    status : JobInfo
        Job information.

    Methods:
    -------
    __init__(self, **kwargs)
        Initializes a new instance of the SwiftVisibility class.

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
    _api_name = "Visibility"
    _schema = VisibilitySchema
    _get_schema = VisibilityGetSchema

    def __init__(self, **kwargs):
        self.status = JobInfo()
        [setattr(self, k, a) for k, a in kwargs.items()]


# Alias
Visibility = SwiftVisibility
SwiftVisWindow = VisWindow
