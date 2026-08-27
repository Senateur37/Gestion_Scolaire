from django.db import models
from accounts.models import User

class Staff(models.Model):
    class Department(models.TextChoices):
        ACADEMIC = "ACADEMIC", "Académique (Enseignants)"
        ADMIN = "ADMIN", "Administration"
        MAINTENANCE = "MAINTENANCE", "Entretien & Logistique"
        OTHER = "OTHER", "Autre"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    department = models.CharField(max_length=20, choices=Department.choices, default=Department.ACADEMIC)
    designation = models.CharField(max_length=100)
    date_of_joining = models.DateField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.designation}"

class LeaveRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        APPROVED = "APPROVED", "Approuvé"
        REJECTED = "REJECTED", "Refusé"

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='leave_requests')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"Congé: {self.staff.user.get_full_name()} ({self.start_date})"

class Payroll(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='payrolls')
    month = models.DateField(help_text="Sélectionner le premier jour du mois concerné")
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Paie {self.month.strftime('%m/%Y')} - {self.staff.user.get_full_name()}"
