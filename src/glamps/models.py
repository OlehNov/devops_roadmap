from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from addons.mixins.timestamps import TimestampMixin
from categories.models import Category
from glamps.constants import HELP_TEXT_STATUSES, HELP_TEXT_TYPE_GLAMPS
from glamps.validators import (
    validate_glamp_price,
    validate_name_glamp,
    validate_premium_level,
    validate_status,
    validate_type,
    validate_zip_code,
    validate_glamp_description
)
from addons.upload_images.downloaders import ThumbnailStorage, upload_to
from config import settings


User = get_user_model()


class Glamp(TimestampMixin):
    # General info
    glamp_type = models.PositiveSmallIntegerField(
        _("Glamp Type"), help_text=HELP_TEXT_TYPE_GLAMPS, default=None, validators=[validate_type]
    )
    is_active = models.BooleanField(
        _("Is Active"), default=False
    )
    is_hidden = models.BooleanField(
        _("Is Hidden"), default=False
    )
    is_verified = models.BooleanField(
        _("Is Verified"), default=False
    )
    is_approved = models.BooleanField(
        _("Is Approved"), default=False
    )
    rating = models.FloatField(
        _("Rating"),
        default=None,
        null=True,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0),
        ],
    )
    premium_level = models.PositiveSmallIntegerField(
        null=True,
        default=None,
        validators=[validate_premium_level],
    )
    priority = models.FloatField(
        null=True,
        default=None,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(100.0),
        ],
    )
    image = models.ImageField(upload_to=upload_to)
    thumb = ImageSpecField(
        source="image",
        processors=[ResizeToFill(300, 300)],
        format="JPEG",
        options={"quality": settings.QUALITY_THUMB},
        cachefile_storage=ThumbnailStorage()
    )
    name = models.CharField(
        _("Glamp Name"), max_length=225, null=False, blank=False, default=None, validators=[validate_name_glamp]
    )
    slug = models.SlugField(
        _("Slug"), max_length=225, null=True, blank=True, unique=True, default=None
    )
    description = models.TextField(
        _("Description"), max_length=5000, null=False, blank=False, default=None, validators=[validate_glamp_description]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name=_("Category"),
        related_name="glamp_category",
    )
    capacity = models.PositiveSmallIntegerField(
        _("Capacity"), validators=[MinValueValidator(1)], default=None
    )
    price = models.DecimalField(
        _("Price"),
        max_digits=10,
        decimal_places=2,
        default=0.00,
        null=True,
        blank=True,
        help_text=_("Price for one night"),
        validators=[validate_glamp_price]
    )
    status = models.PositiveSmallIntegerField(
        _("Status"), help_text=HELP_TEXT_STATUSES, default=None, validators=[validate_status]
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name=_("Glamp Owner"),
        related_name="glamp_owner",
    )

    # Address
    street = models.CharField(
        _("Street"), max_length=255, null=False, blank=False, default=None
    )
    building_number = models.CharField(
        _("Building Number"),
        max_length=255,
        null=True,
        blank=True,
        default=None,
    )
    apartment = models.CharField(
        _("Apartment"), max_length=25, null=True, blank=True, default=None
    )
    city = models.CharField(_("City"), max_length=255, null=False, blank=False)
    region = models.CharField(
        _("Region"), max_length=255, null=True, blank=True, default=None
    )
    latitude = models.FloatField(
        _("Latitude"),
        default=0.0,
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
        null=True,
        blank=True,
    )
    longitude = models.FloatField(
        _("Longitude"),
        default=0.0,
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
        null=True,
        blank=True,
    )

    # Basic amenities
    heating_system = models.BooleanField(_("Heating System"), default=False)
    cooling_system = models.BooleanField(_("Cooling System"), default=False)
    internet = models.BooleanField(_("Internet"), default=False)
    laundry_services = models.BooleanField(_("Laundry Services"), default=False)
    tv = models.BooleanField(_("TV"), default=False)
    iron = models.BooleanField(_("Iron"), default=False)
    workplace = models.BooleanField(_("Workplace"), default=False)

    # Additional amenities
    pool = models.BooleanField(_("Pool"), default=False)
    spa = models.BooleanField(_("Spa"), default=False)
    jacuzzi = models.BooleanField(_("Jacuzzi"), default=False)
    vat = models.BooleanField(_("Vat"), default=False)
    sauna = models.BooleanField(_("Sauna"), default=False)
    fireplace = models.BooleanField(_("Fireplace"), default=False)
    gazebo = models.BooleanField(_("Gazebo"), default=False)
    terrace = models.BooleanField(_("Terrace"), default=False)
    barbecue_area = models.BooleanField(_("Barbecue Area"), default=False)
    hammocks = models.BooleanField(_("Hammocks"), default=False)
    garden_furniture = models.BooleanField(_("Garden Furniture"), default=False)

    # Activities
    pets_farm = models.BooleanField(_("Pets/Farm"), default=False)
    riding = models.BooleanField(_("Riding"), default=False)
    hiking_walking = models.BooleanField(_("Hiking/Walking"), default=False)
    fishing = models.BooleanField(_("Fishing"), default=False)
    swimming = models.BooleanField(_("Swimming"), default=False)
    boating = models.BooleanField(_("Boating"), default=False)
    alpine_skiing = models.BooleanField(_("Alpine Skiing Activities"), default=False)
    meditation_yoga = models.BooleanField(_("Meditation/Yoga"), default=False)
    sports_area = models.BooleanField(_("Sports Area"), default=False)
    game_area = models.BooleanField(_("Game Area"), default=False)
    events_excursions = models.BooleanField(_("Events And Excursions"), default=False)

    # Nature and surroundings
    national_park = models.BooleanField(_("National Park"), default=False)
    sea = models.BooleanField(_("Sea"), default=False)
    lake = models.BooleanField(_("Lake"), default=False)
    stream = models.BooleanField(_("River/Stream"), default=False)
    waterfall = models.BooleanField(_("Waterfall"), default=False)
    thermal_springs = models.BooleanField(_("Thermal Springs"), default=False)
    mountains = models.BooleanField(_("Mountains"), default=False)
    salt_caves = models.BooleanField(_("Salt Caves"), default=False)
    beautiful_views = models.BooleanField(_("Beautiful Views"), default=False)

    # Bedroom
    number_of_bedrooms = models.PositiveSmallIntegerField(
        _("Number Of Bedrooms"), default=None
    )
    number_of_beds = models.PositiveSmallIntegerField(
        _("Number Of Beds"), default=None
    )
    cot_for_babies = models.BooleanField(_("Cot For Babies"), default=False)
    number_of_bathrooms = models.PositiveSmallIntegerField(
        _("Number Of Bathrooms"), default=None
    )
    bathroom_in_room = models.BooleanField(_("Bathroom In The Room"), default=False)

    # Kitchen
    kitchen_in_room = models.BooleanField(_("Kitchen In The Room"), default=False)
    dining_area = models.BooleanField(_("Dining area"), default=False)
    microwave = models.BooleanField(_("Microwave"), default=False)
    plate = models.BooleanField(_("Plate"), default=False)
    refrigerator = models.BooleanField(_("Refrigerator"), default=False)
    kitchen_on_territory = models.BooleanField(
        _("Kitchen On The Territory"), default=False
    )
    no_kitchen = models.BooleanField(_("No Kitchen"), default=False)
    breakfast_included = models.BooleanField(
        _("Breakfast Is Included"), default=False
    )
    lunch_included = models.BooleanField(_("Lunch Is Included"), default=False)
    dinner_included = models.BooleanField(_("Dinner Is Included"), default=False)
    all_inclusive = models.BooleanField(_("All Inclusive"), default=False)
    room_service = models.BooleanField(_("Room service"), default=False)
    bar = models.BooleanField(_("Bar"), default=False)
    restaurant = models.BooleanField(_("Restaurant"), default=False)

    # Booking options
    instant_booking = models.BooleanField(_("Instant Booking"), default=False)
    reception_24 = models.BooleanField(_("24-Hour Reception Desk"), default=False)
    free_cancellation = models.BooleanField(_("Free cancellation"), default=False)

    # Conditions Of Sstay
    allowed_with_animals = models.BooleanField(
        _("Allowed With Animals"), default=False
    )
    suitable_for_children = models.BooleanField(
        _("Suitable For Children"), default=False
    )
    suitable_for_groups = models.BooleanField(_("Suitable For Groups"), default=False)

    # Transport
    can_order_transfer = models.BooleanField(
        _("You Can Order A Transfer"), default=False
    )
    car_charging_station = models.BooleanField(
        _("Car Charging Station"), default=False
    )
    place_for_car = models.BooleanField(_("A Place For A Car"), default=False)

    # Business and events
    projector_and_screen = models.BooleanField(
        _("Projector And Screen"), default=False
    )
    area_for_events = models.BooleanField(_("Area For Events"), default=False)

    # Security
    territory_under_protection = models.BooleanField(
        _("The Territory Is Under Protection"), default=False
    )
    cloakroom = models.BooleanField(_("Cloakroom"), default=False)

    # Accessibility
    without_thresholds = models.BooleanField(_("Without Thresholds"), default=False)
    no_ladder = models.BooleanField(_("No Ladder"), default=False)
    bath_with_handrails = models.BooleanField(_("Bath With Handrails"), default=False)
    toilet_with_handrails = models.BooleanField(
        _("Toilet With Handrails"), default=False
    )
    shower_chair = models.BooleanField(_("Shower Chair"), default=False)
    suitable_for_guests_in_wheelchairs = models.BooleanField(
        _("Suitable For Guests In Wheelchairs"), default=False
    )
    room_on_first_flor = models.BooleanField(
        _("The Room Is Completely Located On The First Floor"), default=False
    )
    zip_code = models.CharField(
        _("Index"), max_length=255, validators=[validate_zip_code], default=False
    )
    single_beds = models.PositiveSmallIntegerField(
        _("Single Beds"), null=True, blank=True, default=None
    )
    double_beds = models.PositiveSmallIntegerField(
        _("Double Beds"), null=True, blank=True, default=None
    )
    guests = models.PositiveSmallIntegerField(
        _("Guests"), null=True, blank=True, default=None
    )
    checkin_time = models.TimeField(
        _("Check-in Time"), null=True, blank=True, default=None
    )
    checkout_time = models.TimeField(
        _("Check-out Time"), null=True, blank=True, default=None
    )
    smoking_allowed = models.BooleanField(
        _("Smoking Allowed"), default=False
    )
    parties_allowed = models.BooleanField(
        _("Parties Allowed"), default=False
    )
    winter = models.BooleanField(
        _("Winter"), default=False
    )
    spring = models.BooleanField(
        _("Spring"), default=False
    )
    summer = models.BooleanField(
        _("Summer"), default=False
    )
    autumn = models.BooleanField(
        _("Autumn"), default=False
    )
    earnings_owner = models.DecimalField(
        _("Earnings"), max_digits=10, decimal_places=2, null=True, blank=True, default=None
    )
    earnings_base_price = models.DecimalField(
        _("Base Price"), max_digits=10, decimal_places=2, null=True, blank=True, default=None
    )
    earnings_tourist_taxes = models.DecimalField(
        _("Tourist Tax"), max_digits=10, decimal_places=2, null=True, blank=True, default=None
    )
    earnings_platform_fee = models.DecimalField(
        _("Platform Fee"), max_digits=10, decimal_places=2, null=True, blank=True, default=None
    )
    terms_agreed = models.BooleanField(
        _("Terms Agreed"), default=False
    )
    title = models.CharField(
        _("Title"), max_length=255, null=True, blank=True, default=None
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


class ImageList(models.Model):
    images_list = models.ImageField(upload_to=upload_to)
    parent = models.ForeignKey(Glamp, on_delete=models.CASCADE, related_name="images_list", default=None, null=True)
    thumbs_list = ImageSpecField(
        source="images_list",
        processors=[ResizeToFill(300, 300)],
        format="JPEG",
        options={"quality": settings.QUALITY_THUMB},
        cachefile_storage=ThumbnailStorage(),
    )
