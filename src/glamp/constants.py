import re
from enum import IntEnum


class GlampStatus(IntEnum):
    UNREGISTERED = 1
    MODERATED = 2
    ACTIVE = 3
    INACTIVE = 4


STATUS = "1: Незареєстрований, 2: Проходить Модерацію, 3: Активний, 4: Закритий"

LOOKUP_SEP = "__"

FILTER_PATTERN = re.compile(r"filters\[(.*?)\]\[(.*?)\]=([^&]*)")

OPERATORS = {
    "$eq": "exact",
    "$eqi": "iexact",
    "$lt": "lt",
    "$lte": "lte",
    "$gt": "gt",
    "$gte": "gte",
    "$in": "in",
    "$null": "isnull",
    "$notnull": "isnull",
    "$contains": "contains",
    "$containsi": "icontains",
    "$between": "range",
    "$startsWith": "startswith",
    "$startsWithi": "istartswith",
    "$endsWith": "endswith",
    "$endsWithi": "iendswith",
    "$regex": "regex",
    "$regexi": "iregex",
}
