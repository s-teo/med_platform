from django.contrib import admin
from django import forms
from .models import (
    Doctor,
    TimeSlot,
    DoctorReview,
    Specialty
)

class DoctorAdminForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
        widgets = {
            'specialty': forms.CheckboxSelectMultiple,
        }

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    form = DoctorAdminForm
    list_display = ('user', 'display_specialties', 'experience_years')
    search_fields = ('user__username', 'user__email', 'specialty__name',)
    list_filter = ('specialty',)

    def display_specialties(self, obj):
        return ", ".join(s.name for s in obj.specialty.all())
    display_specialties.short_description = 'Specialties'

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'id', 'start_time',)
    list_filter = ('doctor',)

@admin.register(DoctorReview)
class DoctorReviewAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'rating', 'created_at')
    search_fields = ('doctor__user__email', 'patient__email',)


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    serch_fields = ('name',)