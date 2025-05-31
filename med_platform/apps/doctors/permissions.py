# apps/appointments/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class IsReviewOwnerOrReadOnly(BasePermission):
    """
    Позволяет владельцу отзыва редактировать его,
    а всем остальным — только читать.
    """
    def has_object_permission(self, request, view, obj):
        # Все могут читать
        if request.method in SAFE_METHODS:
            return True
        # Редактировать может только автор (пациент)
        return obj.patient == request.user


