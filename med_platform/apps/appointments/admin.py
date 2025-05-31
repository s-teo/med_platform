from django.contrib import admin
from .models import Appointment
from django import forms  # обязательно

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    form = AppointmentForm  # если используешь форму
    list_display = ('patient', 'doctor', 'time_slot', 'status')
    list_filter = ('status', 'doctor')
    search_fields = ('patient__email', 'doctor__user__email',)
