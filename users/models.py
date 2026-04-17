from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    tier = models.CharField(
        max_length=20,
        choices=[('free', 'Free'), ('pro', 'Pro')],
        default='free',
        help_text="User subscription tier"
    )

    def __str__(self):
        return self.username