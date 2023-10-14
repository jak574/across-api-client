from marshmallow import Schema, fields, validates_schema, ValidationError
from astropy.coordinates import Longitude, Latitude
from astropy.units import Quantity, deg
from typing import Union, Optional


def coord_convert(
    coord: Union[float, int, str, Quantity, Longitude, None]
) -> Optional[float]:
    """Convert coordinates of various types either string, integer,
    astropy Longitude or astropy "deg" unit, to a float.

    Parameters
    ----------
    coord : Union[float, str, int, Quantity, Longitude, None]
        Coordinate in one of the types

    Returns
    -------
    float | None
        Coordinate expressed as a float. Just pass through a None.
    """
    print(type(coord), coord)
    if coord is None:
        return None
    if type(coord) is Quantity:
        return coord.to(deg).value
    if type(coord) is Longitude or type(coord) is Latitude:
        return coord.value
    # Universal translator
    return float(coord)


class Coordinate(fields.Float):
    def _serialize(self, value, attr, obj, **kwargs) -> Optional[float]:
        return coord_convert(value)


class CoordSchema(Schema):
    ra = Coordinate()
    dec = Coordinate()

    @validates_schema
    def coord_check(self, data, **kwargs):
        """Validate RA/Dec coordinates are within valid ranges.

        Parameters
        ----------
        data : dict
            Schema data

        Raises
        ------
        ValidationError
            Returned if RA/Dec coordinates are not within valid ranges
        """
        if "ra" in data and "dec" in data:
            ra = coord_convert(data["ra"])
            dec = coord_convert(data["dec"])
            if ra is not None and dec is not None:
                if ra >= 0 and ra <= 360 and dec >= -90 and dec <= 90:
                    pass
                else:
                    raise ValidationError("RA/Dec not in valid range.")
