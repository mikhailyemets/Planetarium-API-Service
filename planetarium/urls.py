from django.urls import path, include
from rest_framework import routers
from planetarium.views import (
    ShowThemeView,
    AstronomyShowViewSet
)


app_name = "planetarium"

router = routers.SimpleRouter()


router.register("show_themes", ShowThemeView)
router.register("astronomy_shows", AstronomyShowViewSet)

urlpatterns = [path("", include(router.urls))]