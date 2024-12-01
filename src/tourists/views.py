from drf_spectacular.utils import extend_schema
from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework.viewsets import ModelViewSet
from addons.mixins.eventlog import EventLogMixin
from tourists.models import Tourist


User = get_user_model()


@extend_schema("tourist")
class TouristViewSet(ModelViewSet, EventLogMixin):
    queryset = Tourist.objects.all()
    serializer_class = None
    lookup_url_kwarg = "tourist_id"
    permission_classes = None
