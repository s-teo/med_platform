from rest_framework import serializers
from .models import Appointment
from apps.doctors.models import TimeSlot, Doctor
from django.contrib.auth import get_user_model

User = get_user_model()


class TimeSlotNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'doctor', 'start_time', 'is_booked']


class DoctorNestedSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'full_name', 'specialty', 'phone']


class PatientNestedSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'phone', 'email']


class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientNestedSerializer(read_only=True)
    doctor = DoctorNestedSerializer(read_only=True)
    time_slot = serializers.PrimaryKeyRelatedField(queryset=TimeSlot.objects.all(), write_only=True)
    time_slot_data = TimeSlotNestedSerializer(source='time_slot', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'status', 'time_slot', 'time_slot_data', 'created_at']
        read_only_fields = ['status', 'created_at', 'doctor', 'patient']


class AppointmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['status']  # Позволяет изменять статус, например, отменить запись




