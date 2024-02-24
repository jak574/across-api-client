from datetime import datetime
from enum import Enum
import json
from typing import List, Optional

from pydantic import FilePath, model_validator

from ..base.schema import (
    BaseSchema,
    OptionalCoordSchema,
    OptionalDateRangeSchema,
)


class TOOReason(str, Enum):
    """Reasons for rejecting TOO observations"""

    saa = "In SAA"
    earth_occult = "Earth occulted"
    moon_occult = "Moon occulted"
    sun_occult = "Sun occulted"
    too_old = "Too old"
    other = "Other"
    none = "None"


class TOOStatus(str, Enum):
    """Status of a BurstCubeTOO Request"""

    requested = "Requested"
    rejected = "Rejected"
    declined = "Declined"
    approved = "Approved"
    executed = "Executed"
    other = "Other"


class BurstCubeTOOCoordSchema(OptionalCoordSchema):
    """Schema for BurstCubeTOO coordinates with optional error"""

    error: Optional[float] = None


class BurstCubeTriggerInfo(BaseSchema):
    """
    Metadata schema for the BurstCube Target of Opportunity (TOO) request. Note
    that this schema is not strictly defined, keys are only suggested, and
    additional keys can be added as needed.
    """

    trigger_name: Optional[str] = None
    trigger_mission: Optional[str] = None
    trigger_instrument: Optional[str] = None
    trigger_id: Optional[str] = None
    trigger_duration: Optional[float] = None
    classification: Optional[str] = None
    justification: Optional[str] = None

    class Config:
        extra = "allow"

    @model_validator(mode="before")
    def convert_json_string_to_dict(cls, data):
        if isinstance(data, str):
            return json.loads(data)
        return data


class BurstCubeTOOSchema(BurstCubeTOOCoordSchema):
    """
    Schema to retrieve all information about a BurstCubeTOO Request

    Parameters
    ----------
    id : Optional[int], optional
        The ID of the BurstCubeTOO Request, by default None
    created_by : str
        The username associated with the BurstCubeTOO Request
    created_on : Optional[datetime], optional
        The timestamp of the BurstCubeTOO Request, by default None
    modified_by : Optional[str], optional
        The username associated with the last modification of the BurstCubeTOO
        Request, by default None
    modified_on : Optional[datetime], optional
        The timestamp of the last modification of the BurstCubeTOO Request, by
        default None
    trigger_time : datetime
        The time of the trigger
    trigger_info
        Metadata about the trigger encoded as a Dict, with BurstCubeTriggerInfo as
        a suggested, but not enforced, schema
    exposure : float, optional
        The exposure time for the BurstCubeTOO observation, by default 200
    offset : float, optional
        The offset from `trigger_time` for when the BurstCubeTOO data should
        begin, by default -50
    reason : TOOReason, optional
        The reason for the BurstCubeTOO Request, by default TOOReason.none
    status : TOOStatus, optional
        The status of the BurstCubeTOO Request, by default TOOStatus.requested
    too_info : str, optional
        Additional information about the BurstCubeTOO Request, by default ""
    """

    id: Optional[str] = None
    created_by: str
    created_on: datetime
    modified_by: Optional[str] = None
    modified_on: Optional[datetime] = None
    trigger_time: datetime
    trigger_info: BurstCubeTriggerInfo
    exposure: datetime
    offset: datetime
    reject_reason: TOOReason = TOOReason.none
    status: TOOStatus = TOOStatus.requested
    too_info: str = ""
    healpix_filename: Optional[FilePath] = None


class BurstCubeTOODelSchema(BaseSchema):
    """
    Schema for BurstCubeTOO DELETE API call.

    Attributes
    ----------
    id : int
        The ID of the BurstCubeTOODel object.
    """

    id: str


class BurstCubeTOOPostSchema(BurstCubeTOOCoordSchema):
    """
    Schema to submit a TOO request for BurstCube.

    Parameters
    ----------
    trigger_time : datetime
        The time of the trigger.
    trigger_info : BurstCubeTriggerInfo
        Metadata about the trigger.
    begin : datetime, optional
        The beginning time of the trigger, default is None.
    end : datetime, optional
        The end time of the trigger, default is None.
    exposure : float, optional
        The exposure time, default is 200.
    offset : float, optional
        The offset value, default is -50.
    healpix_filename : Optional[FilePath], optional
        The filename of the healpix file, default is None.
    """

    trigger_time: datetime
    trigger_info: BurstCubeTriggerInfo
    exposure: int = 200
    offset: int = -50
    healpix_filename: Optional[FilePath] = None


class BurstCubeTOOGetSchema(BaseSchema):
    """
    Schema for BurstCubeTOO GET request.

    Parameters
    ----------
    id : int
        The ID of the BurstCube TOO.
    """

    id: str


class BurstCubeTOOPutSchema(BurstCubeTOOPostSchema):
    """
    Schema for BurstCubeTOO GET request.

    Parameters
    ----------
    id : int
        The ID of the BurstCube TOO.
    """

    id: str


class BurstCubeTOORequestsGetSchema(OptionalDateRangeSchema):
    """
    Schema for GET requests to retrieve BurstCube Target of Opportunity (TOO) requests.

    Parameters:
    -----------
    begin
        The start time of the TOO requests.
    end
        The end time of the TOO requests.
    limit
        The maximum number of TOO requests to retrieve.
    """

    length: Optional[float] = None
    limit: Optional[int] = None

    @model_validator(mode="after")
    def check_begin_and_end_or_length_set(self):
        if self.begin is not None and self.end is not None and self.length is not None:
            raise ValueError("Cannot set both begin and end and length.")
        elif self.begin is not None and self.length is not None:
            self.end = self.begin + self.length
        elif self.begin is None and self.end is None and self.length is not None:
            self.end = datetime.utcnow()
            self.begin = self.end - self.length


class BurstCubeTOORequestsSchema(BaseSchema):
    """
    Schema for BurstCube TOO requests.

    Attributes
    ----------
    entries
        List of BurstCube TOOs.
    """

    entries: List[BurstCubeTOOSchema]
