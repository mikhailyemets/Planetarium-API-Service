from django.conf import settings
from django.db import models


class ShowTheme(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Show Theme"
        verbose_name_plural = "Show Themes"


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    theme = models.ManyToManyField(ShowTheme, related_name="shows")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Astronomy Show"
        verbose_name_plural = "Astronomy Shows"
        ordering = ["title", "theme"]


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return f"{self.name} : {self.rows}x{self.seats_in_row}"

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    class Meta:
        verbose_name = "Planetarium"
        verbose_name_plural = "Planetariums"
        ordering = ["name"]


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(
        AstronomyShow,
        on_delete=models.CASCADE,
        related_name="sessions"
    )
    planetarium_dome = models.ForeignKey(
        PlanetariumDome,
        on_delete=models.CASCADE,
        related_name="sessions"
    )
    show_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"{self.astronomy_show} in "
                f"{self.planetarium_dome} at {self.show_time}")

    class Meta:
        ordering = ["show_time"]


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(
        ShowSession,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    def __str__(self):
        return (f"Ticket for {self.show_session} at "
                f"{self.show_session.show_time} : "
                f"{self.row}x{self.seat}")