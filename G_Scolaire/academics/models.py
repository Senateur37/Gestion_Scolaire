# academics/models.py

from django.db import models
from students.models import Student
from teachers.models import Teacher


class SchoolClass(models.Model):
    LEVEL_CHOICES = [(i, f"Année {i}") for i in range(1, 13)]
    level = models.IntegerField(choices=LEVEL_CHOICES, default=1, verbose_name="Niveau d'année (1-12)")
    section = models.CharField(max_length=10, blank=True, verbose_name="Section / Groupe (ex: A, B, C)")
    name = models.CharField(max_length=100, blank=True, verbose_name="Nom complet (Optionnel)")
    academic_year = models.CharField(max_length=20)
    main_teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        base = f"Niveau {self.level}"
        if self.section:
            base += f" {self.section}"
        if self.name:
            base += f" - {self.name}"
        return f"{base} ({self.academic_year})"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE
    )
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "school_class")


class Course(models.Model):
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE
    )
    day = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50, blank=True)