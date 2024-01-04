from across_client.base.fov import FOVCheckBase

from .constants import MISSION
from .schema import SwiftFOVCheckGetSchema, SwiftFOVCheckSchema


class SwiftFOVCheck(FOVCheckBase):
    """
    Class representing a Swift FOV Check.
    """

    _mission = MISSION
    _schema = SwiftFOVCheckSchema
    _get_schema = SwiftFOVCheckGetSchema


# Alias
FOVCheck = SwiftFOVCheck
