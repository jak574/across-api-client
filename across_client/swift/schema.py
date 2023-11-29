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
    """
    Represents a Swift plan entry.

    Attributes:
        roll (float): The roll value.
        obsid (str): The observation ID.
        targetid (int): The target ID.
        segment (int): The segment value.
        xrtmode (int): The XRT mode.
        uvotmode (int): The UVOT mode.
        batmode (int): The BAT mode.
        merit (int): The merit value.
    """

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


class SwiftPlanSchema(PlanSchemaBase):
    """
    Represents a Swift plan schema.

    Attributes:
        entries (List[SwiftPlanEntry]): List of Swift plan entries.
    """

    entries: List[SwiftPlanEntry]  # type: ignore


class SwiftPoint(PointBase):
    roll: Optional[float]


class SwiftPointingSchema(PointingSchemaBase):
    pass


class SwiftPointingGetSchema(PointingGetSchemaBase):
    pass


class SwiftObsEntry(PlanEntryBase):
    """
    Represents a Swift observation entry.

    Attributes:
        slew : int
            The slew value.
        roll : float
            The roll value.
        obsid : str
            The observation ID.
        targetid : int
            The target ID.
        segment : int
            The segment value.
        xrtmode : int
            The XRT mode.
        uvotmode : int
            The UVOT mode.
        batmode : int
            The BAT mode.
        merit : int
            The merit value.
    """

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


class SwiftObservationsPutSchema(UserSchema):
    entries: List[SwiftObsEntry]
    pass


class SwiftObservationsSchema(PlanSchemaBase):
    """
    Schema for Swift observations.
    """

    entries: List[SwiftObsEntry]  # type: ignore


class SwiftFOVCheckGetSchema(BaseSchema):
    """
    Schema for the Swift FOV Check Get request.

    Parameters
    ----------
    ra : float
        Right Ascension coordinate.
    dec : float
        Declination coordinate.
    begin : datetime
        Start time of the observation.
    end : datetime
        End time of the observation.
    stepsize : int, optional
        Step size in seconds for the observation (default is 60).
    earthoccult : bool, optional
        Flag indicating whether to consider Earth occultation (default is True).
    """

    ra: float
    dec: float
    begin: datetime
    end: datetime
    stepsize: int = 60
    earthoccult: bool = True


class SwiftFOVCheckSchema(BaseSchema):
    entries: List[SwiftPoint]
    status: JobInfo
