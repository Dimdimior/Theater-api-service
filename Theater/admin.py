from django.contrib import admin
from .models import (
    Play,
    Actor,
    TheatreHall,
    Performance,
    Ticket,
    Reservation,
    Genre
)

# Register your models here.

admin.register(Play)
admin.register(Actor)
admin.register(TheatreHall)
admin.register(Performance)
admin.register(Ticket)
admin.register(Reservation)
admin.register(Genre)
