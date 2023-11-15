from datetime import datetime
from typing import List, Optional

from ..base.schema import (
    BaseSchema,
    JobInfo,
    PlanEntryBase,
    PlanGetSchemaBase,
    PlanSchemaBase,
    PointBase,
    PointingGetSchemaBase,
    PointingSchemaBase,
    UserSchema,
)


class SwiftPlanEntry(PlanEntryBase):
    roll: float
    obsid: str
    targetid: int
    segment: int
    xrtmode: int
    uvotmode: int
    batmode: int
    merit: int


class SwiftPlanGetSchema(PlanGetSchemaBase):
    pass


class SwiftPlanPutSchema(UserSchema):
    entries: List[SwiftPlanEntry]
    pass


class SwiftPlanSchema(PlanSchemaBase):
    entries: List[SwiftPlanEntry]  # type: ignore


class SwiftPoint(PointBase):
    roll: Optional[float]
    pass


class SwiftPointingSchema(PointingSchemaBase):
    pass


class SwiftPointingGetSchema(PointingGetSchemaBase):
    pass


class SwiftObsEntry(PlanEntryBase):
    slew: int
    roll: float
    obsid: str
    targetid: int
    segment: int
    xrtmode: int
    uvotmode: int
    batmode: int
    merit: int


class SwiftObservationsGetSchema(PlanGetSchemaBase):
    pass


class SwiftObservationsPutSchema(BaseSchema):
    entries: List[SwiftObsEntry]
    pass


class SwiftObservationsSchema(PlanSchemaBase):
    entries: List[SwiftObsEntry]  # type: ignore


class SwiftFOVCheckGetSchema(BaseSchema):
    ra: float
    dec: float
    begin: datetime
    end: datetime
    stepsize: int = 60
    earthoccult: bool = True


class SwiftFOVCheckSchema(BaseSchema):
    entries: List[SwiftPoint]
    status: JobInfo
