from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema

from addons.mixins.eventlog import EventLogMixin

from categories.models import Category
from categories.serializers import CategorySerializer

from roles.permissions import IsAdminOrSuperuser, RoleIsManager

from glamps.permissions import (
    IsAnonymousUser,
    IsGlampOwner,
    RoleIsAdmin,
    RoleIsManager,
    RoleIsOwner,
    RoleIsTourist,
)


@extend_schema(tags=["glamp-categories"])
class CategoryViewSet(ModelViewSet, EventLogMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (RoleIsManager | IsAdminOrSuperuser, )
    lookup_url_kwarg = "category_id"
