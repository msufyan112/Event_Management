from django.contrib import admin
from .models import Event, Registration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'start_datetime', 'capacity', 'available_slots', 'organizer']
    list_filter = ['start_datetime', 'organizer']
    search_fields = ['title', 'location']

    def available_slots(self, obj):
        return obj.available_slots()


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'status', 'registered_at']
    list_filter = ['status', 'event']
    search_fields = ['user__username', 'event__title']