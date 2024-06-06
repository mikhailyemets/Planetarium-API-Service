from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Reservation,
    Ticket
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
    TicketCreateSerializer
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
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        dome = self.request.query_params.get("dome")

        queryset = self.queryset
        if dome:
            queryset = queryset.filter(name__icontains=dome)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PlanetariumDomeListSerializer
        if self.action == "retrieve":
            return PlanetariumDomeRetrieveSerializer

        return super().get_serializer_class()


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