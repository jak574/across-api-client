from datetime import datetime
from enum import Enum
from pydantic import FilePath
from typing import List, Optional


from ..base.schema import (
    BaseSchema,
    JobInfo,
    OptionalCoordSchema,
    PointBase,
    PointingGetSchemaBase,
    PointingSchemaBase,
    UserSchema,
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


class BurstCubeTOOModelSchema(BurstCubeTOOCoordSchema):
    """Schema to retrieve all information about a BurstCubeTOO Request"""

    id: Optional[int] = None
    username: str
    timestamp: Optional[datetime] = None
    trigger_mission: Optional[str] = None
    trigger_instrument: Optional[str] = None
    trigger_id: Optional[str] = None
    trigger_time: Optional[datetime] = None
    trigger_duration: Optional[float] = None
    healpix_filename: Optional[FilePath] = None
    classification: Optional[str] = None
    justification: Optional[str] = None
    begin: Optional[datetime] = None
    end: Optional[datetime] = None
    exposure: float = 200
    offset: float = -50
    reason: TOOReason = TOOReason.none
    too_status: TOOStatus = TOOStatus.requested
    too_info: str


class BurstCubeTOOPutSchema(BurstCubeTOOCoordSchema):
    """Schema to update a BurstCubeTOO Request"""

    id: Optional[int] = None
    username: str
    timestamp: Optional[datetime] = None
    trigger_mission: Optional[str] = None
    trigger_instrument: Optional[str] = None
    trigger_id: Optional[str] = None
    trigger_time: Optional[datetime] = None
    trigger_duration: Optional[float] = None
    classification: Optional[str] = None
    begin: Optional[datetime] = None
    end: Optional[datetime] = None
    exposure: Optional[float] = None
    offset: Optional[float] = None
    reason: TOOReason = TOOReason.none
    too_status: TOOStatus = TOOStatus.requested


class BurstCubeTOODelSchema(BaseSchema):
    """Schema to delete a BurstCubeTOO Request"""

    id: int


class BurstCubeTOOPostSchema(UserSchema, BurstCubeTOOCoordSchema):
    """Schema to create a BurstCubeTOO Request"""

    trigger_mission: str
    trigger_instrument: str
    trigger_id: str
    trigger_time: datetime
    trigger_duration: Optional[float] = None
    healpix_filename: Optional[FilePath] = None
    classification: Optional[str] = None
    justification: Optional[str] = None
    begin: Optional[datetime] = None
    end: Optional[datetime] = None
    exposure: float = 200
    offset: float = -50


class BurstCubeTOOSchema(BurstCubeTOOModelSchema):
    """Schema for the response to a BurstCubeTOO request."""

    status: JobInfo


class BurstCubePoint(PointBase):
    """BurstCube Point"""


class BurstCubePointingSchema(PointingSchemaBase):
    """BurstCube Pointing Schema"""


class BurstCubePointingGetSchema(PointingGetSchemaBase):
    """BurstCube Pointing Get Schema"""


class BurstCubeFOVCheckGetSchema(BaseSchema):
    """BurstCube FOV Check Get Schema"""

    ra: float
    dec: float
    begin: datetime
    end: datetime
    stepsize: int = 60
    earthoccult: bool = True


class BurstCubeFOVCheckSchema(BaseSchema):
    """BurstCube FOV Check Schema"""

    entries: List[BurstCubePoint]
    status: JobInfo


class BurstCubeTOOGetSchema(BaseSchema):
    """BurstCubeTOO Get Schema"""

    id: int


class BurstCubeTOORequestsGetSchema(UserSchema):
    """BurstCubeTOO Requests Get Schema"""

    begin: Optional[datetime] = None
    end: Optional[datetime] = None
    trigger_time: Optional[datetime] = None
    trigger_mission: Optional[str] = None
    trigger_instrument: Optional[str] = None
    trigger_id: Optional[str] = None
    limit: Optional[int] = None
    ra: Optional[float] = None
    dec: Optional[float] = None
    radius: Optional[float] = None


class BurstCubeTOORequestsSchema(BaseSchema):
    """BurstCubeTOO Requests Schema"""

    entries: List[BurstCubeTOOModelSchema]
    status: JobInfo
