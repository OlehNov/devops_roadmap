from enum import IntEnum


class GlampStatus(IntEnum):
    UNREGISTERED = 1
    MODERATED = 2
    ACTIVE = 3
    INACTIVE = 4


class PremiumLevel(IntEnum):
    SILVER = 1
    GOLD = 2
    PLATINUM = 3


class TypeGlamp(IntEnum):
    DOME = 1
    ECO = 2
    SAFARI = 3
    AWNING = 4
    TRIANGULAR = 5
    TENT = 6
    MODULAR = 7
    BARREL = 8
    CONTAINER = 9
    ON_WHEELS = 10
    YURTA = 11
    TREE = 12


HELP_TEXT_STATUSES = "1: Unregister, 2: Moderated, 3: Active, 4: Closed"
HELP_TEXT_TYPE_GLAMPS = (
    "1: DOME, "
    "2: ECO, "
    "3: SAFARI, "
    "4: AWNING, "
    "5: TRIANGULAR, "
    "6: TENT, "
    "7: MODULAR, "
    "8: BARREL, "
    "9: CONTAINER, "
    "10: ON_WHEELS, "
    "11: YURTA, "
    "12: TREE HOUSE",
)
