from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator, \
    MaxValueValidator
from rest_framework import serializers

from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Reservation,
    Ticket
)


class ShowThemeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        validators=[
            RegexValidator(
                regex='^[a-zA-Z]*$',
                message='Only English characters are allowed.',
                code='invalid_name'
            )
        ],
        help_text='Only English characters are allowed.'
    )

    class Meta:
        model = ShowTheme
        fields = ("id", "name")


class AstronomyShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "theme")


class AstronomyShowListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        validators=[
            RegexValidator(
                regex='^[a-zA-Z]*$',
                message='Only English characters are allowed in the title.',
                code='invalid_title'
            )
        ],
        help_text='Only English characters are allowed in the title.'
    )

    description = serializers.CharField(
        validators=[
            RegexValidator(
                regex='^[a-zA-Z]*$',
                message='Only English characters are allowed in the description.',
                code='invalid_description'
            )
        ],
        help_text='Only English characters are allowed in the description.'
    )

    theme = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

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
                regex='^[a-zA-Z]*$',
                message='Only English characters are allowed in the name.',
                code='invalid_name'
            )
        ],
        help_text='Only English characters are allowed in the name.'
    )

    rows = serializers.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(30)
        ]
    )

    seats_in_row = serializers.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(30)
        ]
    )

    price_per_seat = serializers.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('1.00')),
            MinValueValidator(Decimal('30.00'))
        ]
    )
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows",
                  "seats_in_row", "capacity", "price_per_seat")


class PlanetariumDomeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "capacity")


class PlanetariumDomeRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows",
                  "seats_in_row", "capacity", "price_per_seat")


class ShowSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time")


class ShowSessionListSerializer(serializers.ModelSerializer):
    astronomy_show = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="title"
    )
    planetarium_dome = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name"
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
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True
    )

    class Meta:
        model = Reservation
        fields = ["id", "user", "created_at"]
        read_only_fields = ["id", "user", "created_at"]


class ReservationListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="email"
    )
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Reservation
        fields = ("id", "user", "created_at")


class TicketSerializer(serializers.ModelSerializer):

    def validate(self, data):
        row = data.get('row')
        seat = data.get('seat')
        show_session = data.get('show_session')

        planetarium_dome = show_session.planetarium_dome

        for ticket_attr_value, ticket_attr_name, dome_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(planetarium_dome, dome_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise ValidationError(
                    {
                        "Seat already taken": f"{ticket_attr_name} number must be in available range:"
                    }
                )

        return data
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "show_session", "reservation")


class TicketListSerializer(serializers.ModelSerializer):
    show_session = serializers.SerializerMethodField()
    reservation = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    tickets = serializers.SerializerMethodField()

    def get_tickets(self, obj):
        return Ticket.objects.filter(reservation=obj.reservation).count()

    def get_total_price(self, obj):
        return (obj.show_session.planetarium_dome.price_per_seat
                * Ticket.objects.filter(reservation=obj.reservation).count())

    def get_show_session(self, obj):
        return obj.show_session.info

    def get_reservation(self, obj):
        return {
            "id": obj.reservation.id,
            "user": obj.reservation.user.email,
            "created_at": obj.reservation.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat","show_session",
                  "reservation", "total_price", "tickets")


class TicketCreateSerializer(serializers.ModelSerializer):
    reservation = serializers.PrimaryKeyRelatedField(queryset=Reservation.objects.none())

    class Meta:
        model = Ticket
        fields = ["row", "seat", "show_session", "reservation"]

    def __init__(self, *args, **kwargs):
        super(TicketCreateSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            self.fields['reservation'].queryset = Reservation.objects.filter(user=user)

    def create(self, validated_data):
        return Ticket.objects.create(**validated_data)