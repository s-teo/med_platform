from django.contrib import admin
from .models import (
    Doctor,
    TimeSlot,
    DoctorReview
)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'experience_years')
    search_fields = ('user__username', 'user__email', 'specialty',)
    list_filter = ('specialty',)

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'id', 'start_time', 'end_time')
    list_filter = ('doctor',)

@admin.register(DoctorReview)
class DoctorReviewAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'rating', 'created_at')
    search_fields = ('doctor__user__email', 'patient__email',)
