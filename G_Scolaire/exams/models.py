from django.db import models
from academics.models import Subject, Course
from students.models import Student
from accounts.models import User

class ExamSession(models.Model):
    name = models.CharField(max_length=100, help_text="Ex: 1er Trimestre 2026")
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ExamResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='results')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, default=20.0)
    remarks = models.TextField(blank=True)

    class Meta:
        unique_together = ('student', 'subject', 'exam_session')

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.subject.name} - {self.marks_obtained}/{self.total_marks}"
