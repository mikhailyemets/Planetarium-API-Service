from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiExample,
)

from datetime import datetime
from planetarium.serializers import (
    TicketSerializer,
    TicketListSerializer,
    TicketCreateSerializer,
    ShowSessionSerializer,
    ShowSessionListSerializer,
    PlanetariumDomeSerializer,
    AstronomyShowSerializer,
    AstronomyShowRetrieveSerializer,
    AstronomyShowListSerializer,
    ShowThemeSerializer,
)

ticket_schema = extend_schema_view(
    list=extend_schema(
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
                            "created_at": "2022-01-01 00:00:00",
                        },
                        "total_price": "49.99",
                        "tickets": 5,
                    },
                    {
                        "id": 2,
                        "row": 1,
                        "seat": 3,
                        "show_session": "Astronomy Show in Dome at 2022-01-01 12:00:00",
                        "reservation": {
                            "id": 1,
                            "user": "user@example.com",
                            "created_at": "2022-01-01 00:00:00",
                        },
                        "total_price": "49.99",
                        "tickets": 5,
                    },
                ],
            )
        ],
    ),
    create=extend_schema(
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
                name="show_session",
                type=int,
                description="Set the show_session id",
                required=False,
            ),
            OpenApiParameter(
                name="reservation",
                type=int,
                description="You need to choose reservation id that was created by this user",
                required=False,
            ),
        ],
        examples=[
            OpenApiExample(
                "Create Example",
                summary="Example for creating a Ticket instance.",
                description="An example request body for creating a Ticket instance.",
                value={"row": 1, "seat": 2, "show_session": 1, "reservation": 1},
            )
        ],
    ),
    update=extend_schema(
        request=TicketSerializer,
        responses=TicketSerializer,
        examples=[
            OpenApiExample(
                "Update Example",
                summary="Example for updating a Ticket instance.",
                description="An example request body for updating a Ticket instance.",
                value={"row": 1, "seat": 3, "show_session": 1, "reservation": 1},
            )
        ],
    ),
    partial_update=extend_schema(
        request=TicketSerializer,
        responses=TicketSerializer,
        examples=[
            OpenApiExample(
                "Partial Update Example",
                summary="Example for partial updating a Ticket instance.",
                description="An example request body for partial updating a Ticket instance.",
                value={"seat": 4},
            )
        ],
    ),
    retrieve=extend_schema(
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
                            "created_at": "2022-01-01 00:00:00",
                        },
                        "total_price": "49.99",
                        "tickets": 5,
                    },
                ],
            )
        ],
    ),
)

reservation_schema = extend_schema_view(
    create=extend_schema(
        parameters=[
            OpenApiParameter(
                name="user",
                location=OpenApiParameter.QUERY,
                description="Added automatically",
            ),
            OpenApiParameter(
                name="created_at",
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description="Added automatically",
            ),
        ],
    )
)
show_session_schema = extend_schema_view(
    list=extend_schema(
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
                    "astronomy_show": {"title": "Jupiter Show"},
                    "planetarium_dome": {"name": "Jupiter Planetarium"},
                    "date": "2023-10-10",
                    "time": "14:15",
                },
            )
        ],
    ),
    create=extend_schema(
        request=ShowSessionSerializer,
        responses=ShowSessionSerializer,
        parameters=[
            OpenApiParameter(
                name="astronomy_show",
                type=int,
                description="Pick the id of the AstronomyShow",
            ),
            OpenApiParameter(
                name="planetarium_dome",
                type=int,
                description="Pick the id of the PlanetariumDome",
            ),
            OpenApiParameter(
                name="show_time",
                type=datetime,
                description="Enter the show time in " "the format YYYY-MM-DD HH:MM:SS",
            ),
        ],
        examples=[
            OpenApiExample(
                "Create Example",
                summary="Example for creating a ShowSession",
                description="An example request body for creating a ShowSession instance.",
                value={
                    "astronomy_show": 1,
                    "planetarium_dome": 3,
                    "date": "2023-10-10",
                    "show_time": "2024-06-05 17:11:32",
                },
            )
        ],
    ),
    update=extend_schema(
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
                    "show_time": "2024-06-05 17:11:32",
                },
            )
        ],
    ),
    partial_update=extend_schema(
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
    ),
)
pl_dome_schema = extend_schema_view(
    create=extend_schema(
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
                description="The price per seat." "(minimum: 4.00, maximum: 30.00).",
                required=False,
            ),
            OpenApiParameter(
                name="capacity",
                type=int,
                description="The total capacity of the dome" "(derived property).",
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
    ),
    retrieve=extend_schema(
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
    ),
    list=extend_schema(
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
                "for list of a PlanetariumDomes.",
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
    ),
    update=extend_schema(
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
    ),
    partial_update=extend_schema(
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
    ),
)

astronomy_show_schema = extend_schema_view(
    create=extend_schema(
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
                name="theme",
                type={"type": "array", "items": {"type": "integer"}},
                description="The list of ids of the AstronomyShow",
                required=False,
            ),
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
        ],
    ),
    list=extend_schema(
        responses=AstronomyShowListSerializer,
        parameters=[
            OpenApiParameter(
                name="show", type=str, description="Filter shows by title."
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
        ],
    ),
    retrieve=extend_schema(
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
        ],
    ),
    update=extend_schema(
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
        ],
    ),
    partial_update=extend_schema(
        request=AstronomyShowSerializer,
        responses=AstronomyShowSerializer,
        examples=[
            OpenApiExample(
                "Partial Update Example",
                summary="Example for partial updating an AstronomyShow instance.",
                description="An example request body for partial updating an AstronomyShow instance.",
                value={"title": "Partially updated AstronomyShow title"},
            )
        ],
    ),
)

show_theme_schema = extend_schema_view(
    create=extend_schema(
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
    ),
    list=extend_schema(
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
                response_only=True,
            ),
        ],
    ),
)
