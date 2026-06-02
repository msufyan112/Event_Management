from django.urls import path
from .views import (
    EventListCreateView,
    EventDetailView,
    RegisterForEventView,
    MyRegistrationsView,
    CancelRegistrationView,
)

urlpatterns = [
    # Events
    path('events/', EventListCreateView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),

    # Registrations
    path('events/register/', RegisterForEventView.as_view(), name='register-event'),
    path('my-registrations/', MyRegistrationsView.as_view(), name='my-registrations'),
    path('registrations/<int:pk>/cancel/', CancelRegistrationView.as_view(), name='cancel-registration'),
]