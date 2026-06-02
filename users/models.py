from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ATTENDEE = 'attendee', 'Attendee'
        ORGANIZER = 'organizer', 'Organizer'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ATTENDEE,
    )
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True
    )

    def is_organizer(self):
        return self.role == self.Role.ORGANIZER

    def __str__(self):
        return f"{self.username} ({self.role})"