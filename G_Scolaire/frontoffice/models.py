from django.db import models

class VisitorLog(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    purpose = models.TextField()
    person_to_meet = models.CharField(max_length=100)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.check_in.strftime('%Y-%m-%d %H:%M')}"

class AdmissionInquiry(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Ouverte"
        FOLLOW_UP = "FOLLOW_UP", "À relancer"
        CLOSED = "CLOSED", "Fermée/Inscrit"

    parent_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    child_name = models.CharField(max_length=100)
    target_class = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.OPEN)

    def __str__(self):
        return f"Demande pour {self.child_name} ({self.parent_name})"
