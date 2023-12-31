from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        BASIC = "BASIC", 'Basic'
        PREMIUM = "PREMIUM", 'Premium'
        ENTERPRISE = "ENTERPRISE", 'Enterprise'

    base_role = Role.BASIC

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)
