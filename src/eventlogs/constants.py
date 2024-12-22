from enum import IntEnum


class OperationType(IntEnum):
    CREATE = 1
    UPDATE = 2
    DELETE = 3
    CHANGE_STATUS = 4
    ACTIVATED = 5
    DEACTIVATED = 6
    VISIBILITY_CHANGE = 7
    CHANGE_ROLE = 8
    ACTIVATED_PROFILE = 9
    DEACTIVATED_PROFILE = 10
