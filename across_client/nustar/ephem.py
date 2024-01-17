from across_client.base.ephem import EphemBase
from .constants import MISSION


class NuSTAREphem(EphemBase):
    """
    NuSTAREphem class for handling NuSTAR ephemeris data.
    """

    _mission = MISSION


# Alias
Ephem = NuSTAREphem
