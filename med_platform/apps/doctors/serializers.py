from rest_framework import serializers
from .models import Doctor, TimeSlot, DoctorReview


class DoctorSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)


    class Meta:
        model = Doctor
        fields = ['id', 'username','doctor_image', 'full_name', 'specialty', 'bio', 'experience_years',
                  'average_rating']


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
        return DoctorReview.objects.create(
            patient=self.context['request'].user,
            **validated_data
        )

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating', instance.rating)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance