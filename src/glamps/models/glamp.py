from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    DecimalField,
    FloatField,
    ForeignKey,
    Model,
    PositiveIntegerField,
    PositiveSmallIntegerField,
    UUIDField,
)
from django.utils.translation import gettext as _

from categories.models import Category
from glamps.constants import HELP_TEXT_STATUSES, HELP_TEXT_TYPE_GLAMPS
from mixins.timestamps import TimestampMixin


User = get_user_model()


class Glamp(TimestampMixin):
    uuid = UUIDField(
        unique=True,
        default=uuid4,
        primary_key=True,
        editable=False,
    )

    # General info
    glamp_type = PositiveSmallIntegerField(
        _("Glamp Type"), help_text=HELP_TEXT_TYPE_GLAMPS, default=None
    )

    name = CharField(
        _("Glamp Name"), max_length=225, null=False, blank=False, default=None
    )
    description = CharField(
        _("Description"), max_length=5000, null=True, blank=True, default=None
    )
    category = ForeignKey(
        Category,
        on_delete=SET_NULL,
        null=True,
        default=None,
        verbose_name=_("Category"),
        related_name="glamp_category",
    )
    capacity = PositiveSmallIntegerField(
        _("Capacity"), validators=[MinValueValidator(1)], default=None
    )
    price = DecimalField(
        _("Price"),
        max_digits=10,
        decimal_places=2,
        default=0.00,
        null=True,
        blank=True,
        help_text=_("Price for one night"),
    )
    status = PositiveSmallIntegerField(
        _("Status"), help_text=HELP_TEXT_STATUSES, default=None
    )

    owner = ForeignKey(
        User,
        on_delete=CASCADE,
        blank=False,
        null=False,
        verbose_name=_("Glamp Owner"),
        related_name="glamp_owner",
    )

    # Address
    street = CharField(
        _("Street"), max_length=255, null=False, blank=False, default=None
    )
    building_number = CharField(
        _("Building Number"),
        max_length=255,
        null=True,
        blank=True,
        default=None,
    )
    apartment = CharField(
        _("Apartment"), max_length=25, null=True, blank=True, default=None
    )
    city = CharField(_("City"), max_length=255, null=False, blank=False)
    region = CharField(_("Region"), max_length=255, null=True, blank=True, default=None)

    latitude = FloatField(
        _("Latitude"),
        default=0.0,
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
        null=True,
        blank=True,
    )
    longitude = FloatField(
        _("Longitude"),
        default=0.0,
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
        null=True,
        blank=True,
    )

    # Basic amenities
    heating_system = BooleanField(_("Heating System"), default=False)
    cooling_system = BooleanField(_("Cooling System"), default=False)
    internet = BooleanField(_("Internet"), default=False)
    laundry_services = BooleanField(_("Laundry Services"), default=False)
    tv = BooleanField(_("TV"), default=False)
    iron = BooleanField(_("Iron"), default=False)
    workplace = BooleanField(_("Workplace"), default=False)

    # Additional amenities
    pool = BooleanField(_("Pool"), default=False)
    spa = BooleanField(_("Spa"), default=False)
    jacuzzi = BooleanField(_("Jacuzzi"), default=False)
    vat = BooleanField(_("Vat"), default=False)
    sauna = BooleanField(_("Sauna"), default=False)
    fireplace = BooleanField(_("Fireplace"), default=False)
    gazebo = BooleanField(_("Gazebo"), default=False)
    terrace = BooleanField(_("Terrace"), default=False)
    barbecue_area = BooleanField(_("Barbecue Area"), default=False)
    hammocks = BooleanField(_("Hammocks"), default=False)
    garden_furniture = BooleanField(_("Garden Furniture"), default=False)

    # Activities
    pets_farm = BooleanField(_("Pets/Farm"), default=False)
    riding = BooleanField(_("Riding"), default=False)
    hiking_walking = BooleanField(_("Hiking/Walking"), default=False)
    fishing = BooleanField(_("Fishing"), default=False)
    swimming = BooleanField(_("Swimming"), default=False)
    boating = BooleanField(_("Boating"), default=False)
    alpine_skiing = BooleanField(_("Alpine Skiing Activities"), default=False)
    meditation_yoga = BooleanField(_("Meditation/Yoga"), default=False)
    sports_area = BooleanField(_("Sports Area"), default=False)
    game_area = BooleanField(_("Game Area"), default=False)
    events_excursions = BooleanField(_("Events And Excursions"), default=False)

    # Nature and surroundings
    national_park = BooleanField(_("National Park"), default=False)
    sea = BooleanField(_("Sea"), default=False)
    lake = BooleanField(_("Lake"), default=False)
    stream = BooleanField(_("River/Stream"), default=False)
    waterfall = BooleanField(_("Waterfall"), default=False)
    thermal_springs = BooleanField(_("Thermal Springs"), default=False)
    mountains = BooleanField(_("Mountains"), default=False)
    salt_caves = BooleanField(_("Salt Caves"), default=False)
    beautiful_views = BooleanField(_("Beautiful Views"), default=False)

    # Bedroom
    number_of_bedrooms = PositiveSmallIntegerField(
        _("Number Of Bedrooms"), default=None
    )
    number_of_beds = PositiveSmallIntegerField(_("Number Of Beds"), default=None)
    cot_for_babies = BooleanField(_("Cot For Babies"), default=False)
    number_of_bathrooms = PositiveSmallIntegerField(
        _("Number Of Bathrooms"), default=None
    )
    bathroom_in_room = BooleanField(_("Bathroom In The Room"), default=False)

    # Kitchen
    kitchen_in_room = BooleanField(_("Kitchen In The Room"), default=False)
    dining_area = BooleanField(_("Dining area"), default=False)
    microwave = BooleanField(_("Microwave"), default=False)
    plate = BooleanField(_("Plate"), default=False)
    refrigerator = BooleanField(_("Refrigerator"), default=False)
    kitchen_on_territory = BooleanField(_("Kitchen On The Territory"), default=False)
    no_kitchen = BooleanField(_("No Kitchen"), default=False)
    breakfast_included = BooleanField(_("Breakfast Is Included"), default=False)
    lunch_included = BooleanField(_("Lunch Is Included"), default=False)
    dinner_included = BooleanField(_("Dinner Is Included"), default=False)
    all_inclusive = BooleanField(_("All Inclusive"), default=False)
    room_service = BooleanField(_("Room service"), default=False)
    bar = BooleanField(_("Bar"), default=False)
    restaurant = BooleanField(_("Restaurant"), default=False)

    # Booking options
    instant_booking = BooleanField(_("Instant Booking"), default=False)
    reception_24 = BooleanField(_("24-Hour Reception Desk"), default=False)
    free_cancellation = BooleanField(_("Free cancellation"), default=False)

    # Conditions Of Sstay
    allowed_with_animals = BooleanField(_("Allowed With Animals"), default=False)
    suitable_for_children = BooleanField(_("Suitable For Children"), default=False)
    suitable_for_groups = BooleanField(_("Suitable For Groups"), default=False)

    # Transport
    can_order_transfer = BooleanField(_("You Can Order A Transfer"), default=False)
    car_charging_station = BooleanField(_("Car Charging Station"), default=False)
    place_for_car = BooleanField(_("A Place For A Car"), default=False)

    # Business and events
    projector_and_screen = BooleanField(_("Projector And Screen"), default=False)
    area_for_events = BooleanField(_("Area For Events"), default=False)

    # Security
    territory_under_protection = BooleanField(
        _("The Territory Is Under Protection"), default=False
    )
    cloakroom = BooleanField(_("Cloakroom"), default=False)

    # Accessibility
    without_thresholds = BooleanField(_("Without Thresholds"), default=False)
    no_ladder = BooleanField(_("No Ladder"), default=False)
    bath_with_handrails = BooleanField(_("Bath With Handrails"), default=False)
    toilet_with_handrails = BooleanField(_("Toilet With Handrails"), default=False)
    shower_chair = BooleanField(_("Shower Chair"), default=False)
    suitable_for_guests_in_wheelchairs = BooleanField(
        _("Suitable For Guests In Wheelchairs"), default=False
    )
    room_on_first_flor = BooleanField(
        _("The Room Is Completely Located On The First Floor"), default=False
    )

    class Meta:
        db_table = "glamp"
        ordering = ("name",)
        verbose_name = _("Glamp")
        verbose_name_plural = _("Glamps")

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"<GlampModel>: {self.name}"
