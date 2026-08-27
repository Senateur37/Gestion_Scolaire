# attendance/models.py

from django.db import models
from students.models import Student


class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = "PRESENT", "Présent"
        ABSENT = "ABSENT", "Absent"
        LATE = "LATE", "En retard"

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices
    )
    justification = models.TextField(blank=True)

    class Meta:
        unique_together = ("student", "date")