from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from addons.mixins.eventlog import EventLogMixin
from categories.models import Category
from glamps.models import Glamp
from glamps.permissions import (
    IsGlampOwner,
    RoleIsAdmin,
    RoleIsManager,
    RoleIsOwner,
    RoleIsTourist,
)
from glamps.serializers import (
    GlampByCategorySerializer,
    GlampSerializer,
    ActivateGlampSerializer,
    GlampForTouristSerializer,
    GlampForOwnerSerializer,
    GlampForManagerSerializer,
    HiddenGlampSerializer,
    VerifiedGlampSerializer,
    ApprovedGlampSerializer,
    RatingGlampSerializer,
    PremiumLevelGlampSerializer,
    PriorityGlampSerializer
)
from roles.constants import Role


@extend_schema(
    tags=["glamp"],
)
class GlampModelViewSet(ModelViewSet, EventLogMixin):
    queryset = Glamp.objects.all()
    lookup_url_kwarg = "glamp_id"

    def get_permissions(self):
        match self.action:
            case "list":
                permission_classes = [
                    RoleIsAdmin | RoleIsManager | RoleIsTourist | RoleIsOwner
                ]
            case "retrieve":
                permission_classes = [
                    RoleIsAdmin | RoleIsManager | RoleIsOwner | RoleIsTourist
                ]
            case "create":
                permission_classes = [
                    RoleIsAdmin | RoleIsManager | RoleIsOwner
                ]
            case "update":
                permission_classes = [
                    RoleIsAdmin | RoleIsManager | IsGlampOwner
                ]
            case "destroy":
                permission_classes = [
                    RoleIsAdmin | RoleIsManager | IsGlampOwner
                ]
            case "activate":
                permission_classes = [
                    RoleIsAdmin | RoleIsManager
                ]
            case "hidden":
                permission_classes = [
                    RoleIsAdmin | RoleIsManager | RoleIsOwner
                ]
            case "verified":
                permission_classes = [
                    RoleIsAdmin | RoleIsManager
                ]
            case "approved":
                permission_classes = [
                    RoleIsAdmin | RoleIsManager
                ]
            case "rating":
                permission_classes = [
                    RoleIsAdmin | RoleIsManager | RoleIsOwner | RoleIsTourist
                ]
            case "premium_level":
                permission_classes = [
                    RoleIsAdmin | RoleIsManager
                ]
            case "priority":
                permission_classes = [
                    RoleIsAdmin
                ]
            case _:
                permission_classes = []

        return [permission() for permission in permission_classes]

    @extend_schema(
        description=(
            "Retrieve a list of glamps with optional filters. "
            "Filters are applied dynamically based on query parameters. \n\n"
            "**!!! Warning !!!** \n\n"
            "**Filters without special keyword and operators do not work. In this case, you will always receive an empty list.** \n\n"
            "Supported keywords: \n\n"
            "`filters` - **Keyword that define a filter functionality**\n\n"
            "Supported operators: \n\n"
            "`$eq` - **Equal**\n\n"
            "  - `GET http://localhost:8181/api/v1/glamps/?filters[name][$eq]=Glemp 14` \n\n"
            "`$eqi` - **Equal (case-insensitive)**\n\n"
            "  - `GET http://localhost:8181/api/v1/glamps/?filters[name][$eqi]=glemp 14` \n\n"
            "`$lt` - **Less than**\n\n"
            "  - `GET http://localhost:8181/api/v1/glamps/?filters[capacity][$lt]=5` \n\n"
            "  - `GET http://localhost:8181/api/v1/glamps/?filters[price][$lt]=1400` \n\n"
            "`$lte` - **Less than or equal to**\n\n"
            "  - `GET http://localhost:8181/api/v1/glamps/?filters[capacity][$lte]=10` \n\n"
            "  - `GET http://localhost:8181/api/v1/glamps/?filters[price][$lte]=10000` \n\n"
            "`$gt` - **Greater than**\n\n"
            "  - `GET http://localhost:8181/api/v1/glamps/?filters[capacity][$gt]=5` \n\n"
            "  - `GET http://localhost:8181/api/v1/glamps/?filters[price][$gt]=1400` \n\n"
            "`$gte` - **Greater than or equal to**\n\n"
            "  - `GET http://localhost:8181/api/v1/glamps/?filters[capacity][$gte]=5` \n\n"
            "  - `GET http://localhost:8181/api/v1/glamps/?filters[price][$gte]=1400` \n\n"
            "`$in` - **Included in an array**\n\n"
            "  - `GET http://localhost:8181/api/v1/glamps/?filters[city][$in]=Одеса,Буковель` \n\n"
            "`$contains` - **Contains**\n\n"
            "- `GET http://localhost:8181/api/v1/glamps/?filters[name][$contains]=Glemp` \n\n"
            "- `GET http://localhost:8181/api/v1/glamps/?filters[description][$contains]=Luxury` \n\n"
            "`$containsi` - **Contains (case-insensitive)**\n\n"
            "- `GET http://localhost:8181/api/v1/glamps/?filters[name][$containsi]=gLeMp` \n\n"
            "- `GET http://localhost:8181/api/v1/glamps/?filters[description][$containsi]=LuXuRy` \n\n"
            "`$between` - **in range(1, 2)**\n\n"
            "- `GET http://localhost:8181/api/v1/glamps/?filters[price][$between]=1000,5000` \n\n"
            "`$startsWith` - **Starts with**\n\n"
            "- `GET http://localhost:8181/api/v1/glamps/?filters[name][$startsWith]=Glemp` \n\n"
            "`$startsWithi` - **Starts with (case-insensitive)**\n\n"
            "- `GET http://localhost:8181/api/v1/glamps/?filters[name][$startsWithi]=GleMP` \n\n"
            "`$endsWith` - **Ends with**\n\n"
            "- `GET http://localhost:8181/api/v1/glamps/?filters[name][$endsWith]=Welcome` \n\n"
            "`$endsWithi` - **Ends with (case-insensitive)**\n\n"
            "- `GET http://localhost:8181/api/v1/glamps/?filters[name][$endsWithi]=WeLcomE` \n\n"
            'You can also combine fields with "&" symbol for more precise filtering: \n\n'
            "- `GET http://localhost:8181/api/v1/glamps/?filters[city][$in]=Одеса,Буковель&?filters[heating_system][$eq]=1&?filters[price][$gte]=950` \n\n"
            "For fields with **bool** type you can use operator **[$eq]** or **[$eqi]** and values 1 and 0: \n\n"
            "- `0 - False` \n\n"
            "- `1 - True` \n\n"
            "List of fields with **bool** type: \n\n"
            "- `heating_system` \n\n"
            "- `cooling_system` \n\n"
            "- `internet` \n\n"
            "- `laundry_services` \n\n"
            "- `tv` \n\n"
            "- `iron` \n\n"
            "- `workplace` \n\n"
            "- `pool` \n\n"
            "- `spa` \n\n"
            "- `jacuzzi` \n\n"
            "- `vat` \n\n"
            "- `sauna` \n\n"
            "- `fireplace` \n\n"
            "- `gazebo` \n\n"
            "- `terrace` \n\n"
            "- `barbecue_area` \n\n"
            "- `hammocks` \n\n"
            "- `garden_furniture` \n\n"
            "- `pets_farm` \n\n"
            "- `riding` \n\n"
            "- `hiking_walking` \n\n"
            "- `fishing` \n\n"
            "- `swimming` \n\n"
            "- `boating` \n\n"
            "- `alpine_skiing` \n\n"
            "- `meditation_yoga` \n\n"
            "- `sports_area` \n\n"
            "- `game_area` \n\n"
            "- `events_excursions` \n\n"
            "- `national_park` \n\n"
            "- `sea` \n\n"
            "- `lake` \n\n"
            "- `stream` \n\n"
            "- `waterfall` \n\n"
            "- `thermal_springs` \n\n"
            "- `mountains` \n\n"
            "- `salt_caves` \n\n"
            "- `beautiful_views` \n\n"
            "- `cot_for_babies` \n\n"
            "- `bathroom_in_room` \n\n"
            "- `kitchen_in_room` \n\n"
            "- `dining_area` \n\n"
            "- `microwave` \n\n"
            "- `plate` \n\n"
            "- `refrigerator` \n\n"
            "- `kitchen_on_territory` \n\n"
            "- `no_kitchen` \n\n"
            "- `breakfast_included` \n\n"
            "- `lunch_included` \n\n"
            "- `dinner_included` \n\n"
            "- `all_inclusive` \n\n"
            "- `room_service` \n\n"
            "- `bar` \n\n"
            "- `restaurant` \n\n"
            "- `instant_booking` \n\n"
            "- `reception_24` \n\n"
            "- `free_cancellation` \n\n"
            "- `allowed_with_animals` \n\n"
            "- `suitable_for_children` \n\n"
            "- `suitable_for_groups` \n\n"
            "- `can_order_transfer` \n\n"
            "- `car_charging_station` \n\n"
            "- `place_for_car` \n\n"
            "- `projector_and_screen` \n\n"
            "- `area_for_events` \n\n"
            "- `territory_under_protection` \n\n"
            "- `cloakroom` \n\n"
            "- `without_thresholds` \n\n"
            "- `no_ladder` \n\n"
            "- `bath_with_handrails` \n\n"
            "- `toilet_with_handrails` \n\n"
            "- `shower_chair` \n\n"
            "- `suitable_for_guests_in_wheelchairs` \n\n"
            "- `room_on_first_flor` \n\n"
        ),
    )
    def get_serializer_class(self):
        if self.action == "activate":
            return ActivateGlampSerializer
        elif self.action == "hidden":
            return HiddenGlampSerializer
        elif self.action == "verified":
            return VerifiedGlampSerializer
        elif self.action == "approved":
            return ApprovedGlampSerializer
        elif self.action == "rating":
            return RatingGlampSerializer
        elif self.action == "premium_level":
            return PremiumLevelGlampSerializer
        elif self.action == "priority":
            return PriorityGlampSerializer
        elif self.action == "list":
            if self.request.user.role == Role.TOURIST:
                return GlampForTouristSerializer
        elif self.action == "retrieve":
            if self.request.user.role == Role.TOURIST:
                return GlampForTouristSerializer
        elif self.action == "list":
            if self.request.user.role == Role.OWNER:
                return GlampForOwnerSerializer
        elif self.action == "retrieve":
            if self.request.user.role == Role.OWNER:
                return GlampForOwnerSerializer
        elif self.action == "list":
            if self.request.user.role == Role.MANAGER:
                return GlampForManagerSerializer
        elif self.action == "retrieve":
            if self.request.user.role == Role.MANAGER:
                return GlampForManagerSerializer

        return GlampSerializer

    def get_object(self):
        glamp_id = self.kwargs.get("glamp_id")
        return get_object_or_404(Glamp, id=glamp_id)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def perform_create(self, serializer):
        glamp_instance = serializer.save()
        validated_data = serializer.validated_data
        self.log_event(
            self.request,
            operated_object=glamp_instance,
            validated_data=validated_data,
        )
        return glamp_instance

    @transaction.atomic
    def perform_update(self, serializer):
        glamp_instance = serializer.save()
        validated_data = serializer.validated_data
        self.log_event(
            self.request,
            operated_object=glamp_instance,
            validated_data=validated_data,
        )
        return glamp_instance

    @transaction.atomic
    def perform_destroy(self, glamp_instance):
        self.log_event(self.request, operated_object=glamp_instance)
        return super().perform_destroy(glamp_instance)

    @action(detail=True, methods=["put", "patch"])
    def activate(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=kwargs.get("glamp_id"))
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            updated_instance = serializer.save()
            return Response(serializer_class(updated_instance).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["put", "patch"])
    def hidden(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=kwargs.get("pk"))
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            updated_instance = serializer.save()
            return Response(serializer_class(updated_instance).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["put", "patch"])
    def verified(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=kwargs.get("pk"))
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            updated_instance = serializer.save()
            return Response(serializer_class(updated_instance).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["put", "patch"])
    def approved(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=kwargs.get("pk"))
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            updated_instance = serializer.save()
            return Response(serializer_class(updated_instance).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["put", "patch"])
    def rating(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=kwargs.get("pk"))
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            updated_instance = serializer.save()
            return Response(serializer_class(updated_instance).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["put", "patch"])
    def premium_level(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=kwargs.get("pk"))
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            updated_instance = serializer.save()
            return Response(serializer_class(updated_instance).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["put", "patch"])
    def priority(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=kwargs.get("glamp_id"))
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            updated_instance = serializer.save()
            return Response(serializer_class(updated_instance).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["glamp_by_category"],
    parameters=[
        OpenApiParameter(
            "glamp_id",
            OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="The ID of the glamp",
        ),
    ],
)
class GlampByCategoryViewSet(ModelViewSet, EventLogMixin):
    lookup_url_kwarg = "glamp_id"

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        get_object_or_404(Category, id=category_id)
        return Glamp.objects.filter(category_id=category_id)

    def get_permissions(self):
        match self.action:
            case "list":
                permission_classes = [
                    RoleIsAdmin | RoleIsManager | RoleIsTourist | RoleIsOwner
                ]
            case "retrieve":
                permission_classes = [
                    RoleIsAdmin | RoleIsManager | RoleIsOwner | RoleIsTourist
                ]
            case "create":
                permission_classes = [
                    RoleIsAdmin | RoleIsManager | RoleIsOwner
                ]
            case "update":
                permission_classes = [
                    RoleIsAdmin | RoleIsManager | IsGlampOwner
                ]
            case "destroy":
                permission_classes = [
                    RoleIsAdmin | RoleIsManager | IsGlampOwner
                ]
            case "activate":
                permission_classes = [
                    RoleIsAdmin | RoleIsManager
                ]
            case "hidden":
                permission_classes = [
                    RoleIsAdmin | RoleIsManager | RoleIsOwner
                ]
            case "verified":
                permission_classes = [
                    RoleIsAdmin | RoleIsManager
                ]
            case "approved":
                permission_classes = [
                    RoleIsAdmin | RoleIsManager
                ]
            case "rating":
                permission_classes = [
                    RoleIsAdmin | RoleIsManager | RoleIsOwner | RoleIsTourist
                ]
            case "premium_level":
                permission_classes = [
                    RoleIsAdmin | RoleIsManager
                ]
            case "priority":
                permission_classes = [
                    RoleIsAdmin
                ]
            case _:
                permission_classes = []

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "activate":
            return ActivateGlampSerializer
        elif self.action == "hidden":
            return HiddenGlampSerializer
        elif self.action == "verified":
            return VerifiedGlampSerializer
        elif self.action == "approved":
            return ApprovedGlampSerializer
        elif self.action == "rating":
            return RatingGlampSerializer
        elif self.action == "premium_level":
            return PremiumLevelGlampSerializer
        elif self.action == "priority":
            return PriorityGlampSerializer
        elif self.action == "list":
            if self.request.user.role == Role.TOURIST:
                return GlampForTouristSerializer
        elif self.action == "retrieve":
            if self.request.user.role == Role.TOURIST:
                return GlampForTouristSerializer
        elif self.action == "list":
            if self.request.user.role == Role.OWNER:
                return GlampForOwnerSerializer
        elif self.action == "retrieve":
            if self.request.user.role == Role.OWNER:
                return GlampForOwnerSerializer
        elif self.action == "list":
            if self.request.user.role == Role.MANAGER:
                return GlampForManagerSerializer
        elif self.action == "retrieve":
            if self.request.user.role == Role.MANAGER:
                return GlampForManagerSerializer

        return GlampByCategorySerializer

    @transaction.atomic
    def perform_create(self, serializer):
        category_id = self.kwargs.get("category_id")
        category = get_object_or_404(Category, id=category_id)
        glamp_instance = serializer.save(category=category)
        validated_data = serializer.validated_data
        self.log_event(
            self.request,
            operated_object=glamp_instance,
            validated_data=validated_data,
            category=category,
        )
        return glamp_instance

    @transaction.atomic
    def perform_update(self, serializer):
        glamp_instance = serializer.save()
        validated_data = serializer.validated_data
        self.log_event(
            self.request,
            operated_object=glamp_instance,
            validated_data=validated_data,
        )
        return glamp_instance

    @transaction.atomic
    def perform_destroy(self, glamp_instance):
        self.log_event(self.request, operated_object=glamp_instance)
        return super().perform_destroy(glamp_instance)

    @action(detail=True, methods=["put", "patch"])
    def activate(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=kwargs.get("glamp_id"))
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            updated_instance = serializer.save()
            return Response(serializer_class(updated_instance).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["put", "patch"])
    def hidden(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=kwargs.get("pk"))
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            updated_instance = serializer.save()
            return Response(serializer_class(updated_instance).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["put", "patch"])
    def verified(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=kwargs.get("pk"))
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            updated_instance = serializer.save()
            return Response(serializer_class(updated_instance).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["put", "patch"])
    def approved(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=kwargs.get("pk"))
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            updated_instance = serializer.save()
            return Response(serializer_class(updated_instance).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["put", "patch"])
    def rating(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=kwargs.get("pk"))
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            updated_instance = serializer.save()
            return Response(serializer_class(updated_instance).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["put", "patch"])
    def premium_level(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=kwargs.get("pk"))
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            updated_instance = serializer.save()
            return Response(serializer_class(updated_instance).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["put", "patch"])
    def priority(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=kwargs.get("glamp_id"))
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            updated_instance = serializer.save()
            return Response(serializer_class(updated_instance).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
