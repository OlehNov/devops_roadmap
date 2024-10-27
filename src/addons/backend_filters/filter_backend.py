from rest_framework.filters import BaseFilterBackend

from addons.backend_filters.constants import FILTER_PATTERN, LOOKUP_SEP, OPERATORS


class CustomBaseFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_params = {}

        for field, value in request.query_params.items():
            try:
                # Extract field name and operator from the query parameter
                filter_fields = FILTER_PATTERN.findall(f"{field}={value}")[0]
                # filter_fields[0] -> field name
                # filter_fields[1] -> operator for get lookup expressions
                field_name, operator = filter_fields[0], filter_fields[1]
                lookup = LOOKUP_SEP + OPERATORS.get(operator)

                match operator:
                    case "$between":
                        value = tuple(value.strip("()").split(","))
                    case "$in":
                        value = value.strip("()").split(",")

                filter_params[field_name + lookup] = value

            except Exception:
                return []

        return queryset.filter(**filter_params)
