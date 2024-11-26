from django.core.exceptions import FieldError
from rest_framework import filters

from addons.backend_filters.constants import OPERATOR_MAPPING


class SortingFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Retrieve the sorting parameter from the query
        sorting_param = request.query_params.get("sorting")
        if sorting_param:
            # Split the sorting parameter into field and order (default: "asc")
            sort_parts = sorting_param.split(":")
            field = sort_parts[0]
            order = sort_parts[1] if len(sort_parts) > 1 else "asc"
            try:
                # Apply sorting based on the field and order
                queryset = queryset.order_by(f'{"" if order == "asc" else "-"}{field}')
            except FieldError as e:
                # Log the error if the field is invalid
                print(f"Invalid sorting field: {field}. Error: {e}")
                pass
                # queryset = queryset.none()
        return queryset


class QueryParamFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Retrieve all query parameters as a list of tuples
        queried_filters = request.query_params.lists()
        if queried_filters:
            # Parse the filters into a format suitable for Django ORM
            parsed_filters = self._parse_filters(queried_filters)
            try:
                # Apply the parsed filters to the queryset
                queryset = queryset.filter(**parsed_filters)
            except FieldError as e:
                # Log the error if filtering fails
                print(f"Invalid filter field: {e}")
                pass
                # queryset = []
        return queryset

    def _parse_filters(self, queried_filters):
        parsed_filters = {}
        for key, value in queried_filters:
            # Check if the key starts with "filters[" and ends with "]"
            if key.startswith("filters"):
                try:
                    # Split the filter key into parts: field and operator
                    filter_parts = key.split("[")
                    parsed_field = filter_parts[1].strip("]")
                    parsed_operator = filter_parts[2].rstrip("]")

                    # Map the field and operator to Django ORM syntax
                    field = self._get_field(parsed_field)
                    operator = self._get_operator(parsed_operator)
                    value = self._get_value(value)

                    # Add the filter to the parsed filters dictionary
                    if field and operator:
                        parsed_filters[f"{field}__{operator}"] = value
                except IndexError as e:
                    # Log an error if the filter key format is invalid
                    print(f"Invalid filter key format: {key}. Error: {e}")
                    pass
        return parsed_filters

    def _get_field(self, parsed_field):
        # Return the field name as is; add validation if needed
        return parsed_field

    def _get_operator(self, parsed_operator):
        # Map the operator using the operator mapping dictionary
        operator_mapping = OPERATOR_MAPPING
        return operator_mapping.get(parsed_operator)

    def _get_value(self, value):
        # Handle cases where the value is a list with a single item
        if isinstance(value, list) and len(value) == 1:
            return value[0]
        # Return the value as is for other cases
        return value
