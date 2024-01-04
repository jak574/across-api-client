from datetime import datetime

from typing import Optional, Union

from pydantic import FilePath
import io
from ..across.resolve import ACROSSResolveName
from ..base.common import ACROSSBase
from ..base.daterange import ACROSSDateRange
from ..base.schema import JobInfo
from ..base.user import ACROSSUser
from .constants import MISSION
from .schema import (
    BurstCubeTOOGetSchema,
    BurstCubeTOOPostSchema,
    BurstCubeTOOPutSchema,
    BurstCubeTOORequestsGetSchema,
    BurstCubeTOORequestsSchema,
    BurstCubeTOOSchema,
)


class TOO(ACROSSBase, ACROSSUser, ACROSSResolveName, ACROSSDateRange):
    """
    Class representing a Target of Opportunity (TOO) request.

    Parameters:
    ----------
    username : str
        The username of the user making the TOO request.
    api_key : str
        The API key of the user making the TOO request.
    trigger_mission : str
        The mission associated with the TOO request.
    trigger_instrument : str
        The instrument associated with the TOO request.
    trigger_id : str
        The ID of the trigger.
    trigger_time : datetime
        The time of the trigger.
    trigger_duration : float
        The duration of the trigger (s).
    justification : str
        The justification for the TOO request.
    ra : Optional[float]
        The right ascension of the target (optional).
    dec : Optional[float]
        The declination of the target (optional).
    begin : datetime
        The start time of the TOO observation.
    end : datetime
        The end time of the TOO observation.
    exposure : float
        The exposure time for the TOO observation.
    offset : float
        The offset for the TOO observation.
    healpix_filename : Optional[FilePath]
        The healpix filename that represents the object localization for the TOO. This should be a file
        on disk.
    healpix_file : Union[io.BytesIO, io.BufferedReader, None]
        The healpix file handle for the TOO observation, takes a file like object.

    Attributes:
    ----------
    timestamp : datetime
        The time at which the TOO request was made.
    status : JobInfo
        The status of the TOO request.
    too_info : str
        The TOO information, including warnings etc.
    reason : str
        The reason for the TOO request being rejected.
    too_status : str
        The status of the TOO request.
    id : str
        The ID of the TOO request.

    Methods:
    -------
    __init__(self, **kwargs)
        Initializes a new instance of the TOO class.

    """

    trigger_mission: str
    trigger_instrument: str
    trigger_id: str
    trigger_time: datetime
    trigger_duration: Optional[float]
    healpix_filename: Optional[FilePath]
    healpix_file: Union[io.BytesIO, io.BufferedReader, None]
    justification: str
    classification: Optional[str]
    ra: Optional[float]
    dec: Optional[float]
    begin: datetime
    end: datetime
    exposure: float
    offset: float
    status: JobInfo
    too_info: str

    # API definitions

    _mission = MISSION
    _api_name = "TOO"
    _schema = BurstCubeTOOSchema
    _put_schema = BurstCubeTOOPutSchema
    _post_schema = BurstCubeTOOPostSchema
    _get_schema = BurstCubeTOOGetSchema
    _del_schema = BurstCubeTOOGetSchema

    def __init__(self, **kwargs):
        self.exposure = 200
        self.offset = -50

        for k, a in kwargs.items():
            if k in self._schema.model_fields.keys():
                setattr(self, k, a)

    @classmethod
    def submit_too(cls, **kwargs):
        """
        Submit a TOO request.
        """
        cls.status = JobInfo()
        for k, a in kwargs.items():
            if k in cls._post_schema.model_fields.keys():
                setattr(cls, k, a)
            setattr(cls, k, a)
        if cls.validate_post():
            cls.post()

    @property
    def _table(self):
        return (
            [
                "TOO ID",
                "Submitted",
                "Submitter",
                "Trigger Time",
                "Mission",
                "Instrument",
                "ID",
                "Status",
                "Reason",
            ],
            [
                [
                    self.id,
                    self.timestamp,
                    self.username,
                    self.trigger_time,
                    self.trigger_mission,
                    self.trigger_instrument,
                    self.trigger_id,
                    self.too_status.value,
                    self.reason.value,
                ]
            ],
        )


class TOORequests(ACROSSBase, ACROSSUser):
    """
    Represents a Targer of Opportunity (TOO) request.

    Attributes
    ----------
    begin : datetime
        The start time of the observation.
    end : datetime
        The end time of the observation.
    limit : int
        The maximum number of entries for the observation.
    trigger_time : datetime
        The time at which the observation should be triggered.
    entries : list
        The list of entries for the observation.
    status : JobInfo
        The status of the observation.
    """

    _mission = MISSION
    _api_name = "TOORequests"
    _schema = BurstCubeTOORequestsSchema
    _get_schema = BurstCubeTOORequestsGetSchema

    def __init__(self, **kwargs):
        self.entries = []
        for k, a in kwargs.items():
            setattr(self, k, a)
        # As this is a GET only class, we can validate and get the data
        if self.validate_get():
            self.get()

            # Convert the entries to a list of TOO objects
            self.entries = [TOO(**entry.model_dump()) for entry in self.entries]

    @property
    def _table(self):
        return (
            [
                "TOO ID",
                "Submitted",
                "Submitter",
                "Trigger Time",
                "Mission",
                "Instrument",
                "ID",
                "Status",
                "Reason",
            ],
            [
                [
                    entry.id,
                    entry.timestamp,
                    entry.username,
                    entry.trigger_time,
                    entry.trigger_mission,
                    entry.trigger_instrument,
                    entry.trigger_id,
                    entry.too_status.value,
                    entry.reason.value,
                ]
                for entry in self.entries
            ],
        )


# Alias
BurstCubeTOO = TOO
BurstCubeTOORequests = TOORequests
submit_too = TOO.submit_too
burstcube_submit_too = TOO.submit_too
