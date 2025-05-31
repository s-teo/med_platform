from rest_framework import serializers
from .models import Appointment
from apps.doctors.models import TimeSlot



class TimeSlotNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'doctor', 'start_time', 'end_time', 'is_booked']


class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.ReadOnlyField(source='patient.id')
    doctor = serializers.ReadOnlyField(source='time_slot.doctor.id')
    time_slot = serializers.PrimaryKeyRelatedField(queryset=TimeSlot.objects.all(), write_only=True)
    time_slot_data = TimeSlotNestedSerializer(source='time_slot', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'status', 'time_slot', 'time_slot_data', 'created_at']
        read_only_fields = ['status', 'created_at', 'doctor']


class AppointmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['status']  # Позволяет изменять статус, например, отменить запись




