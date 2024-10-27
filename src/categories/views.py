from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from addons.mixins.eventlog import EventLogMixin
from categories.models import Category
from categories.serializers import CategorySerializer
from roles.permissions import IsAdminOrSuperuser, RoleIsManager


@extend_schema(tags=["glamp-categories"])
class CategoryViewSet(EventLogMixin, ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrSuperuser, RoleIsManager)
    # lookup_field = "category_id"
    lookup_url_kwarg = "category_id"
