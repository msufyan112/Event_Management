from rest_framework import serializers
from .models import Event, Registration


# ----------------------------
# EVENT SERIALIZERS
# ----------------------------
class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.StringRelatedField(read_only=True)
    available_slots = serializers.SerializerMethodField()
    is_full = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'location',
            'start_datetime', 'end_datetime', 'capacity',
            'available_slots', 'is_full', 'organizer', 'created_at'
        ]
        read_only_fields = ['organizer', 'created_at']

    def get_available_slots(self, obj):
        return obj.available_slots()

    def get_is_full(self, obj):
        return obj.is_full()

    def validate(self, attrs):
        # end time must be after start time
        if attrs['end_datetime'] <= attrs['start_datetime']:
            raise serializers.ValidationError("End datetime must be after start datetime.")
        return attrs


# ----------------------------
# REGISTRATION SERIALIZERS
# ----------------------------
class RegistrationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)
    event_date = serializers.DateTimeField(source='event.start_datetime', read_only=True)

    class Meta:
        model = Registration
        fields = [
            'id', 'user', 'event', 'event_title',
            'event_date', 'status', 'registered_at'
        ]
        read_only_fields = ['user', 'status', 'registered_at']

    def validate(self, attrs):
        user = self.context['request'].user
        event = attrs['event']

        # Check if event is in the past
        from django.utils import timezone
        if event.start_datetime < timezone.now():
            raise serializers.ValidationError("Cannot register for a past event.")

        # Check if event is full
        if event.is_full():
            raise serializers.ValidationError("This event is fully booked.")

        # Check if user already registered
        if Registration.objects.filter(user=user, event=event, status='confirmed').exists():
            raise serializers.ValidationError("You are already registered for this event.")

        return attrs