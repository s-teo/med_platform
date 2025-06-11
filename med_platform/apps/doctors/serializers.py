from rest_framework import serializers
from .models import Doctor, TimeSlot, DoctorReview, Specialty
from django.contrib.auth import get_user_model

User = get_user_model()


class UserNestedSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'phone']


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['id', 'name']


class DoctorSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    user = UserNestedSerializer(read_only=True)
    specialty = SpecialtySerializer(read_only=True, many=True)  # <-- добавь many=True
    specialty_ids = serializers.PrimaryKeyRelatedField(
        queryset=Specialty.objects.all(), write_only=True, many=True, source='specialty'
    )

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'doctor_image', 'full_name', 'specialty', 'bio', 'experience_years',
                  'average_rating', 'specialty_ids']  # добавь specialty_ids для записи



class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'doctor', 'start_time', 'is_booked']


class TimeSlotCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['start_time', ]

    def create(self, validated_data):
        validated_data.pop('doctor', None)  # удаляем, если вдруг есть
        doctor = self.context['request'].user.doctor_profile
        return TimeSlot.objects.create(doctor=doctor, **validated_data)



class DoctorReviewSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)

    class Meta:
        model = DoctorReview
        fields = ['id', 'doctor', 'patient_name', 'rating', 'comment', 'created_at']


class DoctorReviewCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorReview
        fields = ['doctor', 'rating', 'comment']

    def create(self, validated_data):
        return DoctorReview.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating', instance.rating)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance



