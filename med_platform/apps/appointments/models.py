from django.db import models
from django.conf import settings
from apps.doctors.models import Doctor, TimeSlot  # Импорт из нового приложения

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Запланировано'),
        ('cancelled', 'Отменена'),
        ('completed', 'Завершена'),
    ]
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    time_slot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE)
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} -> {self.doctor} at {self.time_slot.start_time}"

