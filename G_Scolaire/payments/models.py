from django.db import models
from students.models import Student

class Payment(models.Model):
    class Status(models.TextChoices):
        PAID = "PAID", "Payé"
        PARTIAL = "PARTIAL", "Partiel"
        PENDING = "PENDING", "En attente"
        LATE = "LATE", "En retard"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant Total")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Montant Versé")
    due_date = models.DateField()
    payment_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    description = models.CharField(max_length=255)

    @property
    def remaining_amount(self):
        return self.amount - self.amount_paid

    def save(self, *args, **kwargs):
        if self.amount_paid >= self.amount:
            self.status = self.Status.PAID
        elif self.amount_paid > 0:
            self.status = self.Status.PARTIAL
        else:
            self.status = self.Status.PENDING
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - Total: {self.amount} / Versé: {self.amount_paid} ({self.get_status_display()})"
