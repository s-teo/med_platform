from django.urls import path
from .views import (
    DoctorListView,
    AvailableTimeSlotsView,
    DoctorReviewListView,
    DoctorReviewCreateUpdateView,
    TimeSlotCreateView,
    DoctorTimeSlotsView,
    DoctorAppointmentsView,
    SpecialtyListCreateView, DoctorDetailView,
)

urlpatterns = [
    path('', DoctorListView.as_view(), name='doctor-list'),
    path('<int:doctor_id>/slots/', AvailableTimeSlotsView.as_view(), name='available-slots'),
    path('<int:id>/', DoctorDetailView.as_view(), name='doctor-detail'),  # 👈 вот он

    path('<int:doctor_id>/reviews/', DoctorReviewListView.as_view(), name='doctor-reviews'),
    path('reviews/', DoctorReviewCreateUpdateView.as_view(), name='create-or-update-review'),
    path('timeslots/create/', TimeSlotCreateView.as_view(), name='timeslot-create'),
    path('timeslots/', DoctorTimeSlotsView.as_view(), name='doctor-timeslots'),
    path('appointments/', DoctorAppointmentsView.as_view(), name='doctor-appointments'),
    path('specialty/', SpecialtyListCreateView.as_view(), name='specialty-list'),

]
