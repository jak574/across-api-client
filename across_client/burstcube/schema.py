from datetime import datetime
from typing import List, Optional

from ..base.schema import (
    BaseSchema,
    JobStatus,
    OptionalCoordSchema,
    PointBase,
    PointingGetSchemaBase,
    PointingSchemaBase,
    UserSchema,
)


class BurstCubeTOOModelSchema(OptionalCoordSchema):
    """Schema to retrieve all information about a BurstCubeTOO Request"""

    id: Optional[int] = None
    username: str
    timestamp: Optional[datetime] = None
    trigger_mission: Optional[str] = None
    trigger_instrument: Optional[str] = None
    trigger_id: Optional[str] = None
    trigger_time: Optional[datetime] = None
    begin: Optional[datetime] = None
    end: Optional[datetime] = None
    exposure: float = 200
    offset: float = -50


class BurstCubeTOOPutSchema(OptionalCoordSchema):
    """Schema to retrieve all information about a BurstCubeTOO Request"""

    id: Optional[int] = None
    username: str
    timestamp: Optional[datetime] = None
    trigger_mission: Optional[str] = None
    trigger_instrument: Optional[str] = None
    trigger_id: Optional[str] = None
    trigger_time: Optional[datetime] = None
    begin: Optional[datetime] = None
    end: Optional[datetime] = None
    exposure: Optional[float] = None
    offset: Optional[float] = None


class BurstCubeTOODelSchema(BaseSchema):
    id: int


class BurstCubeTOOPostSchema(OptionalCoordSchema):
    """Schema to retrieve all information about a BurstCubeTOO Request"""

    username: str
    timestamp: Optional[datetime] = None
    trigger_mission: str  # Optional[str] = None
    trigger_instrument: str  # Optional[str] = None
    trigger_id: str  # Optional[str] = None
    trigger_time: datetime  # Optional[datetime] = None
    begin: Optional[datetime] = None
    end: Optional[datetime] = None
    exposure: float = 200
    offset: float = -50


class BurstCubeTOOSchema(BurstCubeTOOModelSchema):
    """Schema for the response to a BurstCubeTOO request."""

    status: JobStatus


class BurstCubePoint(PointBase):
    pass


class BurstCubePointingSchema(PointingSchemaBase):
    pass


class BurstCubePointingGetSchema(PointingGetSchemaBase):
    pass


class BurstCubeFOVCheckGetSchema(BaseSchema):
    ra: float
    dec: float
    begin: datetime
    end: datetime
    stepsize: int = 60
    earthoccult: bool = True


class BurstCubeFOVCheckSchema(BaseSchema):
    entries: List[BurstCubePoint]
    status: JobStatus


class BurstCubeTOOGetSchema(BaseSchema):
    id: int


class BurstCubeTOORequestsGetSchema(UserSchema):
    begin: Optional[datetime] = None
    end: Optional[datetime] = None
    trigger_time: Optional[datetime] = None
    limit: Optional[int] = None


class BurstCubeTOORequestsSchema(BaseSchema):
    entries: List[BurstCubeTOOModelSchema]
    status: JobStatus
