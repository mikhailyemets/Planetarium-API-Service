from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from rest_framework import serializers

from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Reservation,
    Ticket,
)


class ShowThemeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        validators=[
            RegexValidator(
                regex="^[a-zA-Z]*$",
                message="Only English characters are allowed.",
                code="invalid_name",
            )
        ],
        help_text="Only English characters are allowed.",
    )

    class Meta:
        model = ShowTheme
        fields = ("id", "name")


class AstronomyShowSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z\s]*$",
                message="Only English characters and spaces are allowed in the title.",
                code="invalid_title",
            )
        ],
        help_text="Only English characters and spaces are allowed in the title.",
    )

    description = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z\s]*$",
                message="Only English characters and spaces are allowed in the description.",
                code="invalid_description",
            )
        ],
        help_text="Only English characters and spaces are allowed in the description.",
    )

    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "theme", "image")


class AstronomyShowListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        validators=[
            RegexValidator(
                regex="^[a-zA-Z]*$",
                message="Only English characters are allowed in the title.",
                code="invalid_title",
            )
        ],
        help_text="Only English characters are allowed in the title.",
    )

    description = serializers.CharField(
        validators=[
            RegexValidator(
                regex="^[a-zA-Z]*$",
                message="Only English characters are allowed in the description.",
                code="invalid_description",
            )
        ],
        help_text="Only English characters are allowed in the description.",
    )

    theme = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "theme")


class AstronomyShowRetrieveSerializer(serializers.ModelSerializer):
    theme = ShowThemeSerializer(many=True, read_only=True)

    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "theme")


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        validators=[
            RegexValidator(
                regex="^[a-zA-Z\s]*$",
                message="Only English characters and spaces are allowed in the name.",
                code="invalid_name",
            )
        ],
        help_text="Only English characters and spaces are allowed in the name.",
    )

    rows = serializers.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(30)]
    )

    seats_in_row = serializers.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(30)]
    )

    price_per_seat = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("1.00")),
            MaxValueValidator(Decimal("30.00")),
        ],
    )

    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows", "seats_in_row", "capacity", "price_per_seat")


class PlanetariumDomeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "capacity")


class PlanetariumDomeRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows", "seats_in_row", "capacity", "price_per_seat")


class ShowSessionSerializer(serializers.ModelSerializer):
    show_time = serializers.DateTimeField(
        help_text="Enter the show time in the format YYYY-MM-DD HH:MM:SS"
    )

    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time")


class ShowSessionListSerializer(serializers.ModelSerializer):
    astronomy_show = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="title"
    )
    planetarium_dome = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )
    show_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time")


class ShowSessionRetrieveSerializer(serializers.ModelSerializer):
    astronomy_show = AstronomyShowRetrieveSerializer(many=False, read_only=True)
    planetarium_dome = PlanetariumDomeRetrieveSerializer(many=False, read_only=True)

    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time")


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Reservation
        fields = ["id", "user", "created_at"]
        read_only_fields = ["id", "user", "created_at"]


class ReservationListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(many=False, read_only=True, slug_field="email")
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Reservation
        fields = ("id", "user", "created_at")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "show_session", "reservation")


class TicketListSerializer(serializers.ModelSerializer):
    show_session_info = serializers.CharField(
        source="show_session.info", read_only=True
    )
    reservation_info = serializers.SerializerMethodField()
    total_price = serializers.DecimalField(
        max_digits=6, decimal_places=2, read_only=True
    )
    tickets = serializers.IntegerField(read_only=True)

    def get_reservation_info(self, obj):
        return {
            "id": obj.reservation.id,
            "user": obj.reservation.user.email,
            "created_at": obj.reservation.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "show_session_info",
            "reservation_info",
            "total_price",
            "tickets",
        )


class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["row", "seat", "show_session", "reservation"]

    def __init__(self, *args, **kwargs):
        super(TicketCreateSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            self.fields["reservation"].queryset = Reservation.objects.filter(user=user)

    def validate(self, data):
        row = data.get("row")
        seat = data.get("seat")
        show_session = data.get("show_session")

        if Ticket.objects.filter(
            show_session=show_session, row=row, seat=seat
        ).exists():
            raise ValidationError("This ticket already exists.")

        planetarium_dome = show_session.planetarium_dome

        for ticket_attr_value, ticket_attr_name, dome_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(planetarium_dome, dome_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise ValidationError(
                    {
                        ticket_attr_name: f"{ticket_attr_name} number must be in available range: (1, {dome_attr_name}): (1, {count_attrs})"
                    }
                )

        return data

    def create(self, validated_data):
        if Ticket.objects.filter(
            show_session=validated_data["show_session"],
            row=validated_data["row"],
            seat=validated_data["seat"],
        ).exists():
            raise ValidationError("This ticket already exists.")

        return Ticket.objects.create(**validated_data)
