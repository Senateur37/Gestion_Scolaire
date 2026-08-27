# teachers/models.py

from django.conf import settings
from django.db import models


class Teacher(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    employee_number = models.CharField(
        max_length=50,
        unique=True
    )
    specialization = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Spécialisation"
    )
    neighborhood = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Quartier"
    )

    def __str__(self):
        return self.user.get_full_name()