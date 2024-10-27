import re


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
    "$is": "iexact",
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
