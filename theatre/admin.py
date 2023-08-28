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

admin.site.register(Play)
admin.site.register(Actor)
admin.site.register(TheatreHall)
admin.site.register(Performance)
admin.site.register(Ticket)
admin.site.register(Reservation)
admin.site.register(Genre)
