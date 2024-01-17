"""
This module contains the definition of various schemas used in the ACROSS API client.

The schemas define the structure and validation rules for different data objects used in the client.
These schemas are used for data serialization, deserialization, and validation.

The module includes the following schemas:
- BaseSchema: Base schema for all other schemas.
- CoordSchema: Schema that defines basic RA/Dec coordinates.
- PositionSchema: Schema that defines position with error.
- OptionalCoordSchema: Schema that defines optional RA/Dec coordinates.
- DateRangeSchema: Schema that defines date range.
- OptionalDateRangeSchema: Schema that defines optional date range.
- UserSchema: Schema for username and API key.
- JobInfo: Schema for ACROSS API Job status.
- VisWindow: Schema for visibility window.
- VisibilitySchema: Schema for visibility entries.
- VisibilityGetSchema: Schema for getting visibility.
- TLEEntry: Schema for TLE entry.
- TLESchema: Schema for TLE.
- SAAEntry: Schema for SAA passage.
- SAASchema: Schema for SAA entries.
- SAAGetSchema: Schema for getting SAA entries.
- PointBase: Schema for spacecraft pointing.
- PointingSchemaBase: Schema for pointing entries.
- PointingGetSchemaBase: Schema for getting pointing entries.
- PlanEntryBase: Schema for plan entry.
- PlanGetSchemaBase: Schema for getting plan entries.
- PlanSchemaBase: Schema for plan entries.
- EphemSchema: Schema for ephemeris entries.
- EphemGetSchema: Schema for getting ephemeris entries.
- MissionSchema: Schema for mission information.
- FOVSchema: Schema for field of view.
- InstrumentSchema: Schema for instrument information.
- EphemConfigSchema: Schema for ephemeris configuration.
- VisibilityConfigSchema: Schema for visibility configuration.
- TLEConfigSchema: Schema for TLE configuration.
- ConfigSchema: Schema for configuration.
"""
from datetime import datetime, timedelta
from typing import Any, List, Optional, Union

import astropy.units as u  # type: ignore
import numpy as np
from astropy.constants import c, h  # type: ignore
from astropy.coordinates import SkyCoord  # type: ignore
from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator
from pydantic_core import Url

from ..functions import convert_to_dt  # type: ignore
from .coords import coord_convert  # type: ignore


class BaseSchema(BaseModel):
    """Base schema for all other schemas"""

    model_config = ConfigDict(from_attributes=True)

    @property
    def _table(self):
        """Get the table representation of the schema"""
        header = self.model_fields.keys()
        return list(header), [list(self.model_dump().values())]


class CoordSchema(BaseSchema):
    """Schema that defines basic RA/Dec"""

    ra: float = Field(ge=0, lt=360)
    dec: float = Field(ge=-90, le=90)

    @model_validator(mode="before")
    @classmethod
    def convert_coord(cls, data: Any) -> Any:
        """Convert the coordinate data to a specific format"""
        if isinstance(data, dict):
            for key in data.keys():
                if key == "ra" or key == "dec":
                    data[key] = coord_convert(data[key])
        else:
            data.ra = coord_convert(data.ra)
            data.dec = coord_convert(data.dec)
        return data

    @property
    def skycoord(self) -> SkyCoord:
        """Get the SkyCoord representation of the coordinates"""
        return SkyCoord(self.ra, self.dec, unit="deg")


class PositionSchema(CoordSchema):
    """Schema that defines position with error"""

    error: Optional[float] = None


class OptionalCoordSchema(BaseSchema):
    """Schema that defines optional RA/Dec"""

    ra: Optional[float] = Field(ge=0, lt=360, default=None)
    dec: Optional[float] = Field(ge=-90, le=90, default=None)

    @model_validator(mode="before")
    @classmethod
    def coord_convert(cls, data: Any) -> Any:
        """Convert the coordinate data to a specific format"""
        if isinstance(data, dict):
            for key in data.keys():
                if key == "ra" or key == "dec":
                    data[key] = coord_convert(data[key])
        elif hasattr(data, "ra") and hasattr(data, "dec"):
            data.ra = coord_convert(data.ra)
            data.dec = coord_convert(data.dec)
        return data

    @model_validator(mode="after")
    @classmethod
    def check_ra_dec(cls, data: Any) -> Any:
        """Check if RA and Dec are both set or both not set"""
        if data.ra is None or data.dec is None:
            assert data.ra == data.dec, "RA/Dec should both be set, or both not set"
        return data

    @property
    def skycoord(self) -> Optional[SkyCoord]:
        """Get the SkyCoord representation of the coordinates"""
        if self.ra is not None and self.dec is not None:
            return SkyCoord(self.ra, self.dec, unit="deg")
        return None


class DateRangeSchema(BaseSchema):
    """Schema that defines date range"""

    begin: datetime
    end: datetime

    @model_validator(mode="before")
    @classmethod
    def convert_date(cls, data: Any) -> datetime:
        """Check if the begin and end dates are both set or both not set"""
        if isinstance(data, dict):
            for key in data.keys():
                if key == "begin" or key == "end":
                    data[key] = convert_to_dt(data[key])
        else:
            data.begin = convert_to_dt(data.begin)
            data.end = convert_to_dt(data.end)
        return data

    @model_validator(mode="after")
    @classmethod
    def check_dates(cls, data: Any) -> Any:
        """Check if the begin and end dates are both set or both not set"""
        assert data.begin <= data.end, "End date should not be before begin."

        return data


class OptionalDateRangeSchema(BaseSchema):
    """Schema that defines optional date range"""

    begin: Optional[datetime] = None
    end: Optional[datetime] = None

    @model_validator(mode="before")
    @classmethod
    def convert_date(cls, data: Any) -> datetime:
        """Check if the begin and end dates are both set or both not set"""
        if isinstance(data, dict):
            for key in data.keys():
                if key == "begin" or key == "end":
                    data[key] = convert_to_dt(data[key])
        else:
            data.begin = convert_to_dt(data.begin)
            data.end = convert_to_dt(data.end)
        return data

    @model_validator(mode="after")
    @classmethod
    def check_dates(cls, data: Any) -> Any:
        """Check if the begin and end dates are both set or both not set"""
        if data.begin is None or data.end is None:
            assert (
                data.begin == data.end
            ), "Begin/End should both be set, or both not set."
        assert data.begin <= data.end, "End date should not be before begin."

        return data


class UserSchema(BaseSchema):
    """Schema for username and API key"""

    username: str
    api_key: str


class VisWindow(DateRangeSchema):
    """Schema for visibility window"""

    initial: str
    final: str


class VisibilitySchema(BaseSchema):
    """Schema for visibility entries"""

    entries: List[VisWindow]


class VisibilityGetSchema(CoordSchema, DateRangeSchema):
    """Schema for getting visibility"""

    hires: Optional[bool] = True


class TLEEntry(BaseSchema):
    """Schema for TLE entry"""

    tle1: str = Field(min_length=69, max_length=69)
    tle2: str = Field(min_length=69, max_length=69)

    @computed_field  # type: ignore
    @property
    def epoch(self) -> datetime:
        """Calculate the epoch of the TLE"""
        tleepoch = self.tle1.split()[3]
        year, dayofyear = int(f"20{tleepoch[0:2]}"), float(tleepoch[2:])
        fracday, dayofyear = np.modf(dayofyear)
        epoch = datetime.fromordinal(
            datetime(year, 1, 1).toordinal() + int(dayofyear) - 1
        ) + timedelta(days=fracday)
        return epoch


class TLESchema(BaseSchema):
    """Schema for TLE"""

    tle: TLEEntry


class SAAEntry(DateRangeSchema):
    """Schema for SAA passage"""

    @property
    def length(self) -> float:
        """Get the length of the passage in seconds"""
        return (self.end - self.begin).total_seconds() / 86400


class SAASchema(BaseSchema):
    """Schema for SAA entries"""

    entries: List[SAAEntry]


class SAAGetSchema(DateRangeSchema):
    """Schema for getting SAA entries"""


class PointBase(BaseSchema):
    """Schema for spacecraft pointing"""

    time: datetime
    ra: Optional[float] = None
    dec: Optional[float] = None
    roll: Optional[float] = None
    observing: bool
    infov: Optional[bool] = None


class PointingSchemaBase(BaseSchema):
    """Schema for pointing entries"""

    entries: List[PointBase]


class PointingGetSchemaBase(DateRangeSchema):
    """Schema for getting pointing entries"""

    stepsize: int = 60


class PlanEntryBase(DateRangeSchema, CoordSchema):
    """Schema for plan entry"""

    targname: str
    exposure: int


class PlanGetSchema(OptionalDateRangeSchema, OptionalCoordSchema):
    """Schema for getting plan entries"""

    obsid: Union[str, int, None] = None
    radius: Optional[float] = None


class PlanSchemaBase(BaseSchema):
    """Schema for plan entries"""

    entries: List[PlanEntryBase]


class EphemSchema(BaseSchema):
    """Schema for ephemeris entries"""

    timestamp: List[datetime] = []
    posvec: List[List[float]]
    earthsize: List[float]
    polevec: Optional[List[List[float]]] = None
    velvec: Optional[List[List[float]]] = None
    sun: List[List[float]]
    moon: List[List[float]]
    latitude: List[float]
    longitude: List[float]
    stepsize: int = 60


class EphemGetSchema(DateRangeSchema):
    """Schema for getting ephemeris entries"""

    stepsize: int = 60


class MissionSchema(BaseSchema):
    """Schema for mission information"""

    name: str
    shortname: str
    agency: str
    type: str
    pi: str
    description: str
    website: Url


class FOVSchema(BaseSchema):
    """Schema for field of view"""

    fovtype: str
    fovarea: float  # degrees**2
    fovparam: Union[str, float, None]
    fovfile: Optional[str] = None


class InstrumentSchema(BaseSchema):
    """Schema for instrument information"""

    name: str
    shortname: str
    description: str
    website: Url
    energy_low: float
    energy_high: float
    fov: FOVSchema

    @property
    def frequency_high(self):
        """Get the high frequency of the instrument"""
        return ((self.energy_high * u.keV) / h).to(u.Hz)  # type: ignore

    @property
    def frequency_low(self):
        """Get the low frequency of the instrument"""
        return ((self.energy_low * u.keV) / h).to(u.Hz)  # type: ignore

    @property
    def wavelength_high(self):
        """Get the high wavelength of the instrument"""
        return c / self.frequency_low.to(u.nm)

    @property
    def wavelength_low(self):
        """Get the low wavelength of the instrument"""
        return c / self.frequency_high.to(u.nm)


class EphemConfigSchema(BaseSchema):
    """Schema for ephemeris configuration"""

    parallax: bool
    apparent: bool
    velocity: bool
    stepsize: int = 60


class VisibilityConfigSchema(BaseSchema):
    """Schema for visibility configuration"""

    earth_cons: bool  # Calculate Earth Constraint
    moon_cons: bool  # Calculate Moon Constraint
    sun_cons: bool  # Calculate Sun Constraint
    ram_cons: bool  # Calculate Ram Constraint
    pole_cons: bool  # Calculate Orbit Pole Constraint
    saa_cons: bool  # Calculate time in SAA as a constraint
    earthoccult: float  # How many degrees from Earth Limb can you look?
    moonoccult: float  # degrees from center of Moon
    sunoccult: float  # degrees from center of Sun
    sunextra: float  # degrees buffer used for planning purpose
    earthextra: float  # degrees buffer used for planning purpose
    moonextra: float  # degrees buffer used for planning purpose


class TLEConfigSchema(BaseSchema):
    """Schema for TLE configuration"""

    tle_bad: float
    tle_url: Optional[Url] = None
    tle_name: str
    tle_heasarc: Optional[Url] = None
    tle_celestrak: Optional[Url] = None


class ConfigSchema(BaseSchema):
    """Schema for configuration"""

    mission: MissionSchema
    instruments: List[InstrumentSchema]
    ephem: EphemConfigSchema
    visibility: VisibilityConfigSchema
    tle: TLEConfigSchema
