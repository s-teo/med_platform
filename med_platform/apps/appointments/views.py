from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Appointment
from .serializers import (
    AppointmentSerializer,
    AppointmentUpdateSerializer,
)
from .permissions import IsAppointmentOwnerOrReadOnly




class AppointmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.filter(
            patient=self.request.user,
            status__in=['scheduled', 'completed']
        )

    def perform_create(self, serializer):
        time_slot = serializer.validated_data.get('time_slot')
        if time_slot.is_booked:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Этот таймслот уже забронирован.")
        # Заставим doctor быть именно тем, что в time_slot
        appointment = serializer.save(patient=self.request.user, doctor=time_slot.doctor)
        time_slot.is_booked = True
        time_slot.save()


class AppointmentUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = AppointmentUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAppointmentOwnerOrReadOnly]
    queryset = Appointment.objects.all()

    def perform_update(self, serializer):
        appointment = serializer.save()
        # Если запись отменена — освобождаем таймслот
        if appointment.status == 'cancelled':
            ts = appointment.time_slot
            ts.is_booked = False
            ts.save()
            appointment.delete()

