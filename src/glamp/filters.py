from django.db.models import QuerySet
from django.http import HttpRequest
from rest_framework.filters import BaseFilterBackend
from rest_framework.views import View
from rest_framework.viewsets import ViewSet

from glamp.constants import FILTER_PATTERN, LOOKUP_SEP, OPERATORS


class CustomBaseFilterBackend(BaseFilterBackend):
    def filter_queryset(
        self, request: HttpRequest, queryset: QuerySet, view: ViewSet | View
    ) -> QuerySet:
        filter_params = {}

        for field, value in request.query_params.items():
            try:
                # Extract field name and operator from the query parameter
                filter_fields = FILTER_PATTERN.findall(f'{field}={value}')[0]
                # filter_fields[0] -> field name
                # filter_fields[1] -> operator for get lookup expressions
                field_name, operator = filter_fields[0], filter_fields[1]
                lookup = LOOKUP_SEP + OPERATORS.get(operator)

                match operator:
                    case 'between':
                        value = tuple(value.strip('()').split(','))
                    case 'in':
                        value = value.strip('()').split(',')
                    case 'null':
                        value = True
                    case 'notnull':
                        value = False

                filter_params[field_name + lookup] = value

            except Exception:
                return []

        return queryset.filter(**filter_params)
