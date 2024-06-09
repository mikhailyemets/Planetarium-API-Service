from datetime import datetime

from django.db.models import Count, Sum, F, Prefetch
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Reservation,
    Ticket,
)

from rest_framework import viewsets, mixins

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


class ShowThemeView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = (IsAdminOrReadOnly,)

    @extend_schema(
        request=ShowThemeSerializer,
        responses=ShowThemeSerializer,
        parameters=[
            OpenApiParameter(
                name="name",
                type=str,
                description="The name of the ShowTheme.",
                required=False,
            ),
        ],
        examples=[
            OpenApiExample(
                "Create Example",
                summary="Example for creating a ShowTheme instance.",
                description="An example request body for"
                            "creating a PlanetariumDome instance.",
                value={
                    "name": "The ShowTheme name",
                },
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        """Create a new ShowTheme instance."""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses=ShowThemeSerializer(many=True),

        examples=[
            OpenApiExample(
                "List Example",
                summary="Example for listing ShowTheme instances.",
                description="An example response body for listing ShowTheme instances.",
                value={
                    "id": 1,
                    "name": "The ShowTheme name 1",
                },
                response_only=True
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        """List ShowTheme instances."""
        return super().list(request, *args, **kwargs)


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

    @extend_schema(
        request=AstronomyShowSerializer,
        responses=AstronomyShowSerializer,
        parameters=[
            OpenApiParameter(
                name="title",
                type=str,
                description="The title of the AstronomyShow.",
                required=False,
            ),
            OpenApiParameter(
                name="description",
                type=str,
                description="The description of the AstronomyShow.",
                required=False,
            ),
            OpenApiParameter(
                name='theme',
                type={"type": "array", "items": {"type": "integer"}},
                description='The list of ids of the AstronomyShow',
                required=False
            )
        ],
        examples=[
            OpenApiExample(
                "Create Example",
                summary="Example for creating an AstronomyShow instance.",
                description="An example request body for creating an AstronomyShow instance.",
                value={
                    "title": "The title of the AstronomyShow",
                    "description": "The description of the AstronomyShow",
                    "theme": [1, 2, 3],
                },
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        """Create a new ShowTheme instance."""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses=AstronomyShowListSerializer,
        parameters=[
            OpenApiParameter(
                name="show",
                type=str,
                description="Filter shows by title."
            )
        ],
        examples=[
            OpenApiExample(
                "Create Example",
                summary="Example for creating an AstronomyShow instance.",
                description="An example request body for creating an AstronomyShow instance.",
                value={
                    "title": "The title of the AstronomyShow",
                    "description": "The description of the AstronomyShow",
                    "theme": ["Galactic Adventure", "Stars and Galaxies"],
                },
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses=AstronomyShowRetrieveSerializer,
        examples=[
            OpenApiExample(
                "Create Example",
                summary="Example for creating an AstronomyShow instance.",
                description="An example request body for creating an AstronomyShow instance.",
                value={
                    "title": "The title of the AstronomyShow",
                    "description": "The description of the AstronomyShow",
                    "theme": ["Galactic Adventure", "Stars and Galaxies"],
                },
            )
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        request=AstronomyShowSerializer,
        responses=AstronomyShowSerializer,
        examples=[
            OpenApiExample(
                "Update Example",
                summary="Example for updating an AstronomyShow instance.",
                description="An example request body for updating an AstronomyShow instance.",
                value={
                    "title": "Updated AstronomyShow title",
                    "description": "Updated description of the AstronomyShow",
                    "theme": [1, 2, 3],
                },
            )
        ]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        request=AstronomyShowSerializer,
        responses=AstronomyShowSerializer,
        examples=[
            OpenApiExample(
                "Partial Update Example",
                summary="Example for partial updating an AstronomyShow instance.",
                description="An example request body for partial updating an AstronomyShow instance.",
                value={
                    "title": "Partially updated AstronomyShow title"
                },
            )
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

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
        name = request.query_params.get("name")
        queryset = self.queryset

        if name:
            queryset = queryset.filter(name__icontains=name)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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
        show = self.request.query_params.get("astronomy_show")
        dome = self.request.query_params.get("planetarium_dome")

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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="astronomy_show",
                type=str,
                description="Filter by the name of the AstronomyShow",
            ),
            OpenApiParameter(
                name="planetarium_dome",
                type=str,
                description="Filter by the name of the PlanetariumDome",
            ),
        ],
        responses=ShowSessionListSerializer(many=True),
        examples=[
            OpenApiExample(
                "List Example",
                summary="Example for listing ShowSessions",
                description="An example response body"
                            "for listing ShowSession instances.",
                value={
                    "id": 1,
                    "astronomy_show": {
                        "title": "Jupiter Show"
                    },
                    "planetarium_dome": {
                        "name": "Jupiter Planetarium"
                    },
                    "date": "2023-10-10",
                    "time": "14:15",
                }
            )
        ],
    )
    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=ShowSessionSerializer,
        responses=ShowSessionSerializer,
        parameters=[
            OpenApiParameter(
                name="astronomy_show",
                type=str,
            ),
            OpenApiParameter(
                name="planetarium_dome",
                type=str,
            ),
            OpenApiParameter(
                name="show_time",
                type=datetime,
                description="Enter the show time in "
                            "the format YYYY-MM-DD HH:MM:SS",
            ),
        ],
        examples=[
            OpenApiExample(
                "Create Example",
                summary="Example for creating a ShowSession",
                description="An example request body for creating a ShowSession instance.",
                value={
                    "astronomy_show": "Jupiter Show",
                    "planetarium_dome": "Jupiter Planetarium",
                    "date": "2023-10-10",
                    "show_time": "2024-06-05 17:11:32",
                },
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        """Create a new ShowSession instance."""
        return super().create(request, *args, **kwargs)
    @extend_schema(
        request=ShowSessionSerializer,
        responses=ShowSessionSerializer,
        parameters=[
            OpenApiParameter(
                name="astronomy_show",
                type=str,
                description="Updated AstronomyShow name",
            ),
            OpenApiParameter(
                name="planetarium_dome",
                type=str,
                description="Updated PlanetariumDome name",
            ),
        ],
        examples=[
            OpenApiExample(
                "Update Example",
                summary="Example for updating a ShowSession",
                description="An example request body for updating a ShowSession instance.",
                value={
                    "astronomy_show": "Updated Jupiter Show",
                    "planetarium_dome": "Updated Jupiter Dome",
                    "show_time": "2024-06-05 17:11:32"
                },
            )
        ],
    )
    def update(self, request, *args, **kwargs):
        """Update a ShowSession instance."""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        request=ShowSessionSerializer,
        responses=ShowSessionSerializer,
        parameters=[
            OpenApiParameter(
                name="astronomy_show",
                type=str,
                description="Updated AstronomyShow name",
            ),
            OpenApiParameter(
                name="planetarium_dome",
                type=str,
                description="Updated PlanetariumDome name",
            ),
        ],
        examples=[
            OpenApiExample(
                "Partial Update Example",
                summary="Example for partially updating a ShowSession",
                description="An example request body"
                            "for partially updating a ShowSession instance.",
                value={"astronomy_show": "Updated Jupiter Show"},
            )
        ],
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update a ShowSession instance."""
        return super().partial_update(request, *args, **kwargs)


class ReservationViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer
        return super().get_serializer_class()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='user',
                location=OpenApiParameter.QUERY,
                description='Added automatically',
            ),
            OpenApiParameter(
                name='created_at',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Added automatically',
            ),
        ],
    )
    def create(self, request, *args, **kwargs):
        """Create a new Reservation"""
        return super().create(request, *args, **kwargs)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related(
        "show_session__planetarium_dome",
        "show_session__astronomy_show",
        "reservation__user"
    ).prefetch_related(
        "show_session__astronomy_show__theme"
    ).annotate(
        ticket_count=Count('reservation__tickets'),
        total_price=F('show_session__planetarium_dome__price_per_seat') * Count('reservation__tickets')
    )
    serializer_class = TicketListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        if user.is_staff:
            return queryset
        return queryset.filter(reservation__user=user)

    @extend_schema(
        request=TicketCreateSerializer,
        responses=TicketSerializer,
        parameters=[
            OpenApiParameter(
                name="row",
                type=str,
                description="Choose the row number",
                required=False,
            ),
            OpenApiParameter(
                name="seat",
                type=str,
                description="Choose the seat number",
                required=False,
            ),
            OpenApiParameter(
                name='show_session',
                type=int,
                description='Set the show_session id',
                required=False
            ),
            OpenApiParameter(
                name="reservation",
                type=int,
                description="Set the reservation id",
                required=False,
            ),
        ],
        examples=[
            OpenApiExample(
                "Create Example",
                summary="Example for creating a Ticket instance.",
                description="An example request body for creating a Ticket instance.",
                value={
                    "row": 1,
                    "seat": 2,
                    "show_session": 1,
                    "reservation": 1
                },
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses=TicketListSerializer,
        examples=[
            OpenApiExample(
                "List Example",
                summary="Example response for listing Tickets.",
                description="A sample example of a list of Tickets.",
                value=[
                    {
                        "id": 1,
                        "row": 1,
                        "seat": 2,
                        "show_session": "Astronomy Show in Dome at 2022-01-01 12:00:00",
                        "reservation": {
                            "id": 1,
                            "user": "user@example.com",
                            "created_at": "2022-01-01 00:00:00"
                        },
                        "total_price": "49.99",
                        "tickets": 5
                    },
                    {
                        "id": 2,
                        "row": 1,
                        "seat": 3,
                        "show_session": "Astronomy Show in Dome at 2022-01-01 12:00:00",
                        "reservation": {
                            "id": 1,
                            "user": "user@example.com",
                            "created_at": "2022-01-01 00:00:00"
                        },
                        "total_price": "49.99",
                        "tickets": 5
                    }
                ],
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of tickets.
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(
        request=TicketSerializer,
        responses=TicketSerializer,
        examples=[
            OpenApiExample(
                "Update Example",
                summary="Example for updating a Ticket instance.",
                description="An example request body for updating a Ticket instance.",
                value={
                    "row": 1,
                    "seat": 3,
                    "show_session": 1,
                    "reservation": 1
                },
            )
        ]
    )
    def update(self, request, *args, **kwargs):
        """
        Update a ticket instance.
        """
        return super().update(request, *args, **kwargs)

    @extend_schema(
        request=TicketSerializer,
        responses=TicketSerializer,
        examples=[
            OpenApiExample(
                "Partial Update Example",
                summary="Example for partial updating a Ticket instance.",
                description="An example request body for partial updating a Ticket instance.",
                value={
                    "seat": 4
                },
            )
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a ticket instance.
        """
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        responses=TicketSerializer,
        examples=[
            OpenApiExample(
                "List Example",
                summary="Example response for listing Tickets.",
                description="A sample example of a list of Tickets.",
                value=[
                    {
                        "id": 1,
                        "row": 1,
                        "seat": 2,
                        "show_session": "Astronomy Show in Dome at 2022-01-01 12:00:00",
                        "reservation": {
                            "id": 1,
                            "user": "user@example.com",
                            "created_at": "2022-01-01 00:00:00"
                        },
                        "total_price": "49.99",
                        "tickets": 5
                    },
                ],
            )
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
