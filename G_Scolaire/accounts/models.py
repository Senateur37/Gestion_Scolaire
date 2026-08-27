# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrateur"
        TEACHER = "TEACHER", "Enseignant"
        STUDENT = "STUDENT", "Élève"
        PARENT = "PARENT", "Parent"

    role = models.CharField(
        max_length=20,
        choices=Role.choices
    )
    phone = models.CharField(max_length=30, blank=True)