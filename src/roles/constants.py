from enum import IntEnum


class Role(IntEnum):
    ADMIN = 1
    MANAGER = 2
    TOURIST = 3
    OWNER = 4


class ProfileStatus(IntEnum):
    ACTIVATED = 1
    SUSPENDED = 2
    DELETED = 3
    DEACTIVATED = 4
    BANNED = 5


HELP_TEXT_ROLE = "1: ADMIN, 2:MANAGER, 3:TOURIST, 4:OWNER"
HELP_TEXT_PROFILE_STATUS = (
    "1: ACTIVATED, 2: SUSPENDED, 3: DELETED, 4: DEACTIVATED, 5: BANNED"
)
