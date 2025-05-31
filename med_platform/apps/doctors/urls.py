from django.urls import path
from .views import (
    DoctorListView,
    AvailableTimeSlotsView,
    DoctorReviewListView, DoctorReviewCreateUpdateView,
)

urlpatterns = [
    path('', DoctorListView.as_view(), name='doctor-list'),
    path('<int:doctor_id>/slots/', AvailableTimeSlotsView.as_view(), name='available-slots'),
    path('<int:doctor_id>/reviews/', DoctorReviewListView.as_view(), name='doctor-reviews'),
    path('reviews/', DoctorReviewCreateUpdateView.as_view(), name='create-or-update-review'),

]
