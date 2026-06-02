from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_staff']
    list_filter = ['role', 'is_staff']

    # Add role field to the admin edit form
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )