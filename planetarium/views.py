from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import IsAuthenticated
from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Reservation,
    Ticket,
)

from rest_framework import viewsets

from planetarium.permissions import IsAdminOrReadOnly
from planetarium.serializers import (
    ShowThemeSerializer,
    AstronomyShowSerializer,
    AstronomyShowListSerializer,
    AstronomyShowRetrieveSerializer,
    PlanetariumDomeSerializer,
    PlanetariumDomeListSerializer,
    PlanetariumDomeRetrieveSerializer,
    ShowSessionSerializer,
    ShowSessionListSerializer,
    ShowSessionRetrieveSerializer,
    ReservationSerializer,
    ReservationListSerializer,
    TicketSerializer,
    TicketListSerializer,
    TicketCreateSerializer,
)


class ShowThemeView(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = (IsAdminOrReadOnly,)


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.prefetch_related("theme")
    serializer_class = AstronomyShowSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        show = self.request.query_params.get("show")

        queryset = self.queryset

        if show:
            queryset = queryset.filter(title__icontains=show)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return AstronomyShowListSerializer

        if self.action == "retrieve":
            return AstronomyShowRetrieveSerializer

        return super().get_serializer_class()


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return PlanetariumDomeListSerializer

        if self.action == "retrieve":
            return PlanetariumDomeRetrieveSerializer

        return super().get_serializer_class()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                type=str,
                description="The name of the PlanetariumDome.",
                required=False,
            ),
            OpenApiParameter(
                name="rows",
                type=int,
                description="The number of rows in the dome."
                "(minimum: 1, maximum: 20)",
                required=False,
            ),
            OpenApiParameter(
                name="seats_in_row",
                type=int,
                description="The number of seats in each row."
                "(minimum: 1, maximum: 20)",
                required=False,
            ),
            OpenApiParameter(
                name="price_per_seat",
                type=float,
                description="The price per seat."
                            "(minimum: 4.00, maximum: 30.00).",
                required=False,
            ),
            OpenApiParameter(
                name="capacity",
                type=int,
                description="The total capacity of the dome"
                            "(derived property).",
                required=False,
            ),
        ],
        request=PlanetariumDomeSerializer,
        responses=PlanetariumDomeSerializer,
        examples=[
            OpenApiExample(
                "Create Example",
                summary="Example for creating a PlanetariumDome",
                description="An example request body for"
                            "creating a PlanetariumDome instance.",
                value={
                    "name": "Apollo Dome",
                    "rows": 10,
                    "seats_in_row": 20,
                    "price_per_seat": "15.50",
                },
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        """Create a new PlanetariumDome instance."""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses={200: PlanetariumDomeSerializer, 404: "Not Found"},
        examples=[
            OpenApiExample(
                "Retrieve Example",
                summary="Example for retrieving a PlanetariumDome",
                description="An example response body for"
                            "retrieving a PlanetariumDome instance.",
                value={
                    "id": 1,
                    "name": "Apollo Dome",
                    "rows": 10,
                    "seats_in_row": 20,
                    "capacity": 200,
                    "price_per_seat": "15.50",
                },
            )
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve details of a specific PlanetariumDome instance by ID."""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                type=str,
                description="Filter by name of the PlanetariumDome",
            ),
        ],
        responses=PlanetariumDomeSerializer(many=True),
        examples=[
            OpenApiExample(
                "Retrieve Example",
                summary="Example for retrieving a PlanetariumDome",
                description="An example response body"
                            "forretrieving a PlanetariumDome instance.",
                value={
                    "id": 1,
                    "name": "Apollo Dome",
                    "rows": 10,
                    "seats_in_row": 20,
                    "capacity": 200,
                    "price_per_seat": "15.50",
                },
            )
        ],
    )
    def list(self, request, *args, **kwargs):
        """List PlanetariumDomes, with optional filtering by name."""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        request=PlanetariumDomeSerializer,
        responses=PlanetariumDomeSerializer,
        examples=[
            OpenApiExample(
                "Update Example",
                summary="Example for updating a PlanetariumDome",
                description="An example request body for"
                            "updating a PlanetariumDome instance.",
                value={
                    "name": "Apollo Dome Updated",
                    "rows": 12,
                    "seats_in_row": 22,
                    "price_per_seat": "16.50",
                },
            )
        ],
    )
    def update(self, request, *args, **kwargs):
        """Update a PlanetariumDome instance."""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        request=PlanetariumDomeSerializer,
        responses=PlanetariumDomeSerializer,
        examples=[
            OpenApiExample(
                "Partial Update Example",
                summary="Example for partially updating a PlanetariumDome",
                description="An example request body for"
                            "partially updating a PlanetariumDome instance.",
                value={"name": "Apollo Dome Partially Updated"},
            )
        ],
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update a PlanetariumDome instance."""
        return super().partial_update(request, *args, **kwargs)


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.select_related(
        "astronomy_show",
        "planetarium_dome"
    )
    serializer_class = ShowSessionSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        show = self.request.query_params.get("show")
        dome = self.request.query_params.get("dome")

        queryset = self.queryset

        if show:
            queryset = queryset.filter(astronomy_show__title__icontains=show)
        if dome:
            queryset = queryset.filter(planetarium_dome__name__icontains=dome)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializer
        if self.action == "retrieve":
            return ShowSessionRetrieveSerializer

        return super().get_serializer_class()


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer
        return super().get_serializer_class()


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related("show_session", "reservation")
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        elif self.action == "create":
            return TicketCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(reservation__user=user)
