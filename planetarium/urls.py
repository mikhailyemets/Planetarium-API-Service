from django.urls import path, include
from rest_framework import routers
from planetarium.views import (
    ShowThemeView,
    AstronomyShowViewSet,
    PlanetariumDomeViewSet,
    ShowSessionViewSet,
    ReservationViewSet,
    TicketViewSet,
)


app_name = "planetarium"

router = routers.SimpleRouter()


router.register("themes", ShowThemeView)
router.register("shows", AstronomyShowViewSet)
router.register("domes", PlanetariumDomeViewSet)
router.register("show_sessions", ShowSessionViewSet)
router.register("reservations", ReservationViewSet)
router.register("tickets", TicketViewSet)
urlpatterns = [path("", include(router.urls))]
