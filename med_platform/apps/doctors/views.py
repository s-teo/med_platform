from rest_framework import generics, permissions
from .models import Doctor, TimeSlot, DoctorReview
from rest_framework.response import Response
from .permissions import IsReviewOwnerOrReadOnly
from .serializers import (
    DoctorSerializer,
    TimeSlotSerializer,
    DoctorReviewSerializer,
    DoctorReviewCreateUpdateSerializer,
)



class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.AllowAny]


class AvailableTimeSlotsView(generics.ListAPIView):
    serializer_class = TimeSlotSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        doctor_id = self.kwargs.get('doctor_id')
        return TimeSlot.objects.filter(doctor_id=doctor_id, is_booked=False)



class DoctorReviewListView(generics.ListAPIView):
    serializer_class = DoctorReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        doctor_id = self.kwargs['doctor_id']
        return DoctorReview.objects.filter(doctor_id=doctor_id)


class DoctorReviewCreateUpdateView(generics.CreateAPIView):
    serializer_class = DoctorReviewCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsReviewOwnerOrReadOnly]

    def post(self, request, *args, **kwargs):
        doctor_id = request.data.get('doctor')
        existing_review = DoctorReview.objects.filter(doctor_id=doctor_id, patient=request.user).first()

        serializer = self.get_serializer(
            instance=existing_review,
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create_or_update(serializer, existing_review)
        return Response(serializer.data)

    def perform_create_or_update(self, serializer, existing_review):
        if existing_review:
            serializer.save()
        else:
            serializer.save()