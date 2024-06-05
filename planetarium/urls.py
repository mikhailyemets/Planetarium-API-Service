from django.urls import path, include
from rest_framework import routers
from planetarium.views import (
    ShowThemeView,
    AstronomyShowViewSet,
    PlanetariumDomeViewSet,
    ShowSessionViewSet,
    ReservationViewSet
)


app_name = "planetarium"

router = routers.SimpleRouter()


router.register("themes", ShowThemeView)
router.register("shows", AstronomyShowViewSet)
router.register("domes", PlanetariumDomeViewSet)
router.register("show_sessions", ShowSessionViewSet)
router.register("reservations", ReservationViewSet)
urlpatterns = [path("", include(router.urls))]