# apps/appointments/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class IsReviewOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Все могут читать
        if request.method in SAFE_METHODS:
            return True
        # Редактировать может только автор (пациент)
        return obj.patient == request.user

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_doctor
            and hasattr(request.user, 'doctor_profile')
        )