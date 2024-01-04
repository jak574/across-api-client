from across_client.base.fov import FOVCheckBase

from .constants import MISSION
from .schema import BurstCubeFOVCheckGetSchema, BurstCubeFOVCheckSchema


class BurstCubeFOVCheck(FOVCheckBase):
    """
    Class representing a BurstCube FOV Check.
    """

    _mission = MISSION
    _schema = BurstCubeFOVCheckSchema
    _get_schema = BurstCubeFOVCheckGetSchema


# Alias
FOVCheck = BurstCubeFOVCheck
