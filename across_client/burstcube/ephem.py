from across_client.base.ephem import EphemBase
from .constants import MISSION


class BurstCubeEphem(EphemBase):
    """
    BurstCubeEphem class for handling BurstCube ephemeris data.
    """

    _mission = MISSION


# Alias
Ephem = BurstCubeEphem
