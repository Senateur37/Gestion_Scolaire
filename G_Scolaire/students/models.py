# students/models.py

from django.conf import settings
from django.db import models


class Parent(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.get_full_name()


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    GENDER_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    parents = models.ManyToManyField(Parent, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True, verbose_name="Sexe")
    age = models.IntegerField(blank=True, null=True, verbose_name="Âge")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Date de naissance")
    neighborhood = models.CharField(max_length=100, blank=True, verbose_name="Quartier")
    parent_contact = models.CharField(max_length=20, blank=True, verbose_name="Numéro du parent")
    registration_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Matricule"
    )
    address = models.TextField(blank=True, verbose_name="Adresse complète")

    def __str__(self):
        return self.user.get_full_name()