from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Doctor, TimeSlot, DoctorReview
from .permissions import IsReviewOwnerOrReadOnly, IsDoctor
from .serializers import (
    DoctorSerializer,
    TimeSlotSerializer,
    TimeSlotCreateSerializer,
    DoctorReviewSerializer,
    DoctorReviewCreateUpdateSerializer,
)
from apps.appointments.serializers import AppointmentSerializer  # если есть такой сериализатор
from apps.appointments.models import Appointment  # если у тебя записи в другом приложении


class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.AllowAny]


class AvailableTimeSlotsView(generics.ListAPIView):
    serializer_class = TimeSlotSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        doctor_id = self.kwargs.get('doctor_id')
        return TimeSlot.objects.filter(doctor_id=doctor_id, is_booked=False).order_by('start_time')


class DoctorReviewListView(generics.ListAPIView):
    serializer_class = DoctorReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        doctor_id = self.kwargs.get('doctor_id')
        return DoctorReview.objects.filter(doctor_id=doctor_id).order_by('-created_at')


class DoctorReviewCreateUpdateView(generics.GenericAPIView):
    serializer_class = DoctorReviewCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsReviewOwnerOrReadOnly]

    def post(self, request, *args, **kwargs):
        doctor_id = request.data.get('doctor')
        if not doctor_id:
            return Response({"detail": "doctor field is required"}, status=status.HTTP_400_BAD_REQUEST)

        existing_review = DoctorReview.objects.filter(doctor_id=doctor_id, patient=request.user).first()

        serializer = self.get_serializer(
            instance=existing_review,
            data=request.data,
            context={'request': request},
            partial=bool(existing_review)
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create_or_update(serializer, existing_review)
        return Response(serializer.data)

    def perform_create_or_update(self, serializer, existing_review):
        # save обновит существующий отзыв или создаст новый
        serializer.save(patient=self.request.user)


class TimeSlotCreateView(generics.CreateAPIView):
    serializer_class = TimeSlotCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def perform_create(self, serializer):
        # TimeSlotCreateSerializer берет доктора из контекста, но для явности передаем здесь
        serializer.save(doctor=self.request.user.doctor_profile)


class DoctorTimeSlotsView(generics.ListAPIView):
    serializer_class = TimeSlotSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_queryset(self):
        # Показываем все слоты доктора, который делает запрос
        doctor = self.request.user.doctor_profile
        return TimeSlot.objects.filter(doctor=doctor)


class DoctorAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_queryset(self):
        doctor = self.request.user.doctor_profile
        return Appointment.objects.filter(doctor=doctor)