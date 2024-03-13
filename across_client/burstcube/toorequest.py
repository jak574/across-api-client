import io
from datetime import datetime
from typing import Optional, Union

from pydantic import FilePath

from across_client.base.schema import AuthToken

from ..across.resolve import ACROSSResolveName
from ..base.common import ACROSSBase
from ..base.daterange import ACROSSDateRange
from ..base.user import ACROSSUser
from .constants import MISSION
from .schema import (
    BurstCubeTOOGetSchema,
    BurstCubeTOOPostSchema,
    BurstCubeTOOPutSchema,
    BurstCubeTOORequestsGetSchema,
    BurstCubeTOORequestsSchema,
    BurstCubeTOOSchema,
    BurstCubeTriggerInfo,
)


class TOO(ACROSSBase, ACROSSUser, ACROSSResolveName, ACROSSDateRange):
    """
    Class representing a Target of Opportunity (TOO) request.

    Parameters:
    ----------
    credential: AuthToken
        The credential for login obtained from the get_credential function.
    trigger_time : datetime
        The time of the trigger.
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
    trigger_info : BurstCubeTriggerInfo
        The trigger information for the TOO observation.

    Attributes:
    ----------
    timestamp : datetime
        The time at which the TOO request was made.
    too_info : str
        The TOO information, including warnings etc.
    reason : str
        The reason for the TOO request being rejected.
    status : str
        The status of the TOO request.
    id : str
        The ID of the TOO request.

    Methods:
    -------
    __init__(self, **kwargs)
        Initializes a new instance of the TOO class.

    """

    trigger_time: datetime
    healpix_filename: Optional[FilePath]
    healpix_file: Union[io.BytesIO, io.BufferedReader, None]

    ra: Optional[float]
    dec: Optional[float]
    begin: datetime
    end: datetime
    exposure: float
    offset: float
    too_info: str
    trigger_info: BurstCubeTriggerInfo
    credential: Optional[AuthToken]

    # API definitions

    _mission = MISSION
    _api_name = "TOO"
    _schema = BurstCubeTOOSchema
    _put_schema = BurstCubeTOOPutSchema
    _post_schema = BurstCubeTOOPostSchema
    _get_schema = BurstCubeTOOGetSchema
    _del_schema = BurstCubeTOOGetSchema

    def __init__(self, **kwargs):
        self.id = None
        self.exposure = 200
        self.offset = -50

        for k, a in kwargs.items():
            if k in self._schema.model_fields.keys():
                setattr(self, k, a)
        if "credential" in kwargs.keys():
            self.credential = kwargs["credential"]

    @classmethod
    def submit_too(cls, **kwargs):
        """
        Submit a TOO request.
        """
        for k, a in kwargs.items():
            if k in cls._post_schema.model_fields.keys():
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
                    self.created_on,
                    self.created_by,
                    self.trigger_time,
                    self.trigger_info.trigger_mission,
                    self.trigger_info.trigger_instrument,
                    self.trigger_info.trigger_id,
                    self.status.value,
                    self.reject_reason.value,
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
    """

    _mission = MISSION
    _api_name = "TOO"
    _schema = BurstCubeTOORequestsSchema
    _get_schema = BurstCubeTOORequestsGetSchema

    def __init__(self, **kwargs):
        self.entries = []
        self.begin = None
        self.end = None
        self.limit = None
        for k, a in kwargs.items():
            if k in self._get_schema.model_fields.keys():
                setattr(self, k, a)

        # As this is a GET only class, we can validate and get the data
        if self.validate_get():
            self.get()

        # Convert the entries to a list of TOO objects
        # self.entries = [TOO(**entry.model_dump()) for entry in self.entries]

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
                    entry.created_on,
                    entry.created_by,
                    entry.trigger_time,
                    entry.trigger_info.trigger_mission,
                    entry.trigger_info.trigger_instrument,
                    entry.trigger_info.trigger_id,
                    entry.status.value,
                    entry.reject_reason.value,
                ]
                for entry in self.entries
            ],
        )


# Alias
BurstCubeTOO = TOO
BurstCubeTOORequests = TOORequests
submit_too = TOO.submit_too
burstcube_submit_too = TOO.submit_too
