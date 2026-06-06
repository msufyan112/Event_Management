from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Event, Registration
from .serializers import EventSerializer, RegistrationSerializer


# ----------------------------
# CUSTOM PERMISSIONS
# ----------------------------
class IsOrganizerOrReadOnly(permissions.BasePermission):
    """Only organizers can create/edit/delete events."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # anyone can view
        return request.user.is_authenticated and request.user.is_organizer()

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.organizer == request.user  # only the owner can edit/delete


# ----------------------------
# EVENT VIEWS
# ----------------------------
class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsOrganizerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)  # auto-assign organizer


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsOrganizerOrReadOnly]


# ----------------------------
# REGISTRATION VIEWS
# ----------------------------
class RegisterForEventView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Event.objects.all()  # needed for get_object()

    def get_object(self):
        """Fetch the event from URL parameter."""
        event_id = self.kwargs.get('event_id')
        try:
            return Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound("Event not found.")

    def perform_create(self, serializer):
        # Check if user is authenticated
        user = self.request.user
        if not user or not user.is_authenticated:
            raise PermissionDenied("User must be authenticated to register for an event.")
        
        # Get the event from the URL parameter
        event = self.get_object()
        serializer.save(user=user, event=event)  # auto-assign logged-in user and event


class MyRegistrationsView(generics.ListAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Registration.objects.filter(user=self.request.user)  # only my registrations


class CancelRegistrationView(generics.UpdateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Registration.objects.filter(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        registration = self.get_object()

        if registration.status == 'cancelled':
            return Response(
                {"detail": "Registration is already cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )

        registration.status = 'cancelled'
        registration.save()
        return Response(
            {"detail": "Registration cancelled successfully."},
            status=status.HTTP_200_OK
        )