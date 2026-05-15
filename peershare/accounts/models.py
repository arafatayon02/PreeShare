from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    university_email = models.EmailField(
        unique=True, blank=True, default=''
    )
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
