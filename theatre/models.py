import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError


# Create your models here.


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


def play_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)

    filename = f"{slugify(instance.title)}-{uuid.uuid4()}.{extension}"

    return os.path.join("uploads/plays/", filename)


class Play(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, related_name="plays", blank=True)
    actors = models.ManyToManyField(Actor, related_name="plays", blank=True)
    image = models.ImageField(null=True, upload_to=play_image_file_path)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]


class TheatreHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class Performance(models.Model):
    play = models.ForeignKey(
        Play,
        on_delete=models.CASCADE,
        related_name="performance"
    )
    theatre_hall = models.ForeignKey(
        TheatreHall,
        on_delete=models.CASCADE,
        related_name="performance"
    )
    show_time = models.DateTimeField()

    def __str__(self):
        return f"{self.play.title} at {str(self.show_time)} in {self.theatre_hall.name}"


class Reservation(models.Model):
    created_at = models.DateTimeField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return str(self.created_at)


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("performance", "row", "seat")
        ordering = ["row", "seat"]

    def clean(self):
        for ticket_attr_value, ticket_attr_name, theatre_hall_attr_name in [
            (self.row, "row", "rows"),
            (self.seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(
                self.performance.theatre_hall, theatre_hall_attr_name
            )
            if not (1 <= ticket_attr_value <= count_attrs):
                raise ValidationError(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                                          f"number must be in following range: "
                                          f"(1, {theatre_hall_attr_name}): "
                                          f"(1, {count_attrs})"
                    }
                )

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        self.full_clean()
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"{str(self.performance)} (row: {self.row}, seat: {self.seat})"
