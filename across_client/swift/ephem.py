from across_client.base.ephem import EphemBase
from .constants import MISSION


class SwiftEphem(EphemBase):
    """
    SwiftEphem class for handling Swift ephemeris data.
    """

    _mission = MISSION


# Alias
Ephem = SwiftEphem
