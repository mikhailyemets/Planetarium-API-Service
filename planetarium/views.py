from django.db.models import Count, F
from rest_framework.permissions import IsAuthenticated, AllowAny


from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Reservation,
    Ticket,
)

from planetarium.schemas import (
    ticket_schema,
    reservation_schema,
    show_session_schema,
    pl_dome_schema,
    astronomy_show_schema,
    show_theme_schema,
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
    TicketListSerializer,
    TicketCreateSerializer,
)


@show_theme_schema
class ShowThemeView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = (IsAdminOrReadOnly,)


@astronomy_show_schema
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


@pl_dome_schema
class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return PlanetariumDomeListSerializer

        if self.action == "retrieve":
            return PlanetariumDomeRetrieveSerializer

        return super().get_serializer_class()


@show_session_schema
class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.select_related("astronomy_show",
                                                  "planetarium_dome")
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


@reservation_schema
class ReservationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer
        return super().get_serializer_class()


@ticket_schema
class TicketViewSet(viewsets.ModelViewSet):
    queryset = (
        Ticket.objects.select_related(
            "show_session__planetarium_dome",
            "show_session__astronomy_show",
            "reservation__user",
        )
        .prefetch_related("show_session__astronomy_show__theme")
        .annotate(
            ticket_count=Count("reservation__tickets"),
            total_price=F("show_session__planetarium_dome__price_per_seat")
            * Count("reservation__tickets"),
        )
    )

    def get_permissions(self):
        if self.request.query_params.get("telegram_username", None):
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        telegram_username = self.request.query_params.get("telegram_username", None)
        queryset = self.queryset

        if telegram_username:
            return queryset.filter(
                reservation__user__telegram_username=telegram_username
            ).select_related("show_session", "reservation")

        user = self.request.user
        if user.is_staff:
            return queryset
        return queryset.filter(reservation__user=user).select_related(
            "show_session", "reservation"
        )

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        if self.action == "create":
            return TicketCreateSerializer
        return super().get_serializer_class()
