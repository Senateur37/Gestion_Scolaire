# grades/models.py

from django.db import models
from students.models import Student
from academics.models import Subject


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    coefficient = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=1
    )
    exam_type = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    comment = models.TextField(blank=True)