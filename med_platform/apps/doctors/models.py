from django.db import models
from django.conf import settings


class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Specialties"
        ordering = ['id']

    def __str__(self):
        return self.name


class Doctor(models.Model):
    doctor_image = models.ImageField(upload_to='doctors_images', default='doctors_images/default.png', null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile')
    specialty = models.ManyToManyField(Specialty, related_name='doctors')  # <--- так можно несколько
    bio = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)

    def __str__(self):
        specialties = ", ".join([s.name for s in self.specialty.all()])
        return f"Dr. {self.user.get_full_name()} ({specialties}) {self.user.username}"

    @property
    def average_rating(self):
        return self.reviews.aggregate(avg=models.Avg('rating'))['avg'] or 0



class TimeSlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='time_slots')
    start_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor} - {self.start_time}"

class DoctorReview(models.Model):
    doctor = models.ForeignKey(Doctor, related_name='reviews', on_delete=models.CASCADE)
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='doctor_reviews', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], blank=True, null=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'patient')
        ordering = ['-created_at']

    def __str__(self):
        return f"Review for {self.doctor} by {self.patient} - {self.rating}★"

