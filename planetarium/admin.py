from django.contrib import admin
from django.contrib.auth.models import Group

from .models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Reservation,
    Ticket
)


@admin.register(ShowTheme)
class ShowThemeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(AstronomyShow)
class AstronomyShowAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']


@admin.register(PlanetariumDome)
class PlanetariumDomeAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity']


@admin.register(ShowSession)
class ShowSessionAdmin(admin.ModelAdmin):
    list_display = ['astronomy_show', 'planetarium_dome', 'show_time']
    list_filter = ['astronomy_show', 'planetarium_dome']
    search_fields = ['astronomy_show__title', 'planetarium_dome__name']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['show_session', 'row', 'seat', 'reservation']
    list_filter = ['show_session', 'reservation']


admin.site.unregister(Group)