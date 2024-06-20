import os
import uuid
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils.text import slugify


class ShowTheme(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Show Theme"
        verbose_name_plural = "Show Themes"


def show_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/shows/", filename)


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=400)
    theme = models.ManyToManyField(ShowTheme, related_name="shows")
    image = models.ImageField(null=True, upload_to=show_image_file_path)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Astronomy Show"
        verbose_name_plural = "Astronomy Shows"
        ordering = ["id"]


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    price_per_seat = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    class Meta:
        verbose_name = "Planetarium"
        verbose_name_plural = "Planetariums"


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(
        AstronomyShow, on_delete=models.CASCADE, related_name="sessions"
    )
    planetarium_dome = models.ForeignKey(
        PlanetariumDome, on_delete=models.CASCADE, related_name="sessions"
    )
    show_time = models.DateTimeField(
        help_text="Enter the show time in the format YYYY-MM-DD HH:MM:SS"
    )

    @property
    def info(self):
        return (
            f"{self.astronomy_show} in "
            f"{self.planetarium_dome} at "
            f"{self.show_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    def __str__(self):
        if isinstance(self.show_time, str):
            show_time_obj = datetime.strptime(self.show_time, "%Y-%m-%d %H:%M:%S")
        else:
            show_time_obj = self.show_time

        return (
            f"{self.astronomy_show} in "
            f"{self.planetarium_dome} at "
            f"{show_time_obj.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    class Meta:
        ordering = ["show_time"]


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"#{self.id} Reserved by {self.user} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(
        ShowSession, on_delete=models.CASCADE, related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="tickets"
    )

    @staticmethod
    def validate_ticket(row, seat, planetarium_dome, error_to_raise):
        for ticket_attr_value, ticket_attr_name, dome_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(planetarium_dome, dome_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                        f"number must be in available range:"
                        f"(1, {dome_attr_name}): "
                        f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.show_session.planetarium_dome,
            ValidationError,
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):

        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return (
            f"Ticket for {self.show_session} at "
            f"{self.show_session.show_time} : "
            f"{self.row}x{self.seat}"
        )

    class Meta:
        ordering = ["id"]
        unique_together = ("show_session", "row", "seat")
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
