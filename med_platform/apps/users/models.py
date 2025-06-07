from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    phone = models.CharField(max_length=20, unique=True, null=False, blank=False)
    is_phone_verified = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

    def __str__(self):
        return self.username  # или self.email, если email основной
