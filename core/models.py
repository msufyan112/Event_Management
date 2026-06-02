from django.db import models
from django.conf import settings


# ----------------------------
# EVENT MODEL
# ----------------------------
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organized_events'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_datetime']  # upcoming events first

    def is_full(self):
        return self.registrations.filter(status='confirmed').count() >= self.capacity

    def available_slots(self):
        confirmed = self.registrations.filter(status='confirmed').count()
        return self.capacity - confirmed

    def __str__(self):
        return self.title


# ----------------------------
# REGISTRATION MODEL
# ----------------------------
class Registration(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CONFIRMED
    )
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'event']  # one registration per user per event
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.user.username} → {self.event.title} ({self.status})"