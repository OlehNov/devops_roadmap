from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from addons.mixins.eventlog import EventLogMixin
from categories.models import Category
from glamps.models.glamp import Glamp
from categories.serializers import CategorySerializer, GlampByCategoryViewSet
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


@extend_schema(
    tags=["glamp_by_category"],
)
class GlampByCategoryViewSet(ModelViewSet, EventLogMixin):
    serializer_class = GlampByCategoryViewSet
    lookup_url_kwarg = "glamp_id"

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        return Glamp.objects.filter(category_id=category_id)

    def get_permissions(self):
        match self.action:
            case "list", "retrieve":
                permission_classes = [
                    IsAnonymousUser
                    | RoleIsAdmin
                    | RoleIsManager
                    | RoleIsOwner
                    | RoleIsTourist
                ]
            case "create", "update", "destroy":
                permission_classes = [
                    RoleIsAdmin | RoleIsManager | RoleIsOwner
                ]
            case _:
                permission_classes = []

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        category_id = self.kwargs.get("category_id")
        category = Category.objects.get(id=category_id)
        glamp_instance = serializer.save(category=category)
        self.log_event(self.request, glamp_instance)
        return glamp_instance

    def perform_update(self, serializer):
        glamp_instance = serializer.save()
        self.log_event(self.request, glamp_instance)
        return glamp_instance

    def perform_destroy(self, glamp_instance):
        self.log_event(self.request, glamp_instance)
        return super().perform_destroy(glamp_instance)