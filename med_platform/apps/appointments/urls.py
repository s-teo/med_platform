from django.urls import path
from .views import (

    AppointmentListCreateView, AppointmentUpdateView,
)

urlpatterns = [
    path('', AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('<int:pk>/', AppointmentUpdateView.as_view(), name='appointment-update'),
]
