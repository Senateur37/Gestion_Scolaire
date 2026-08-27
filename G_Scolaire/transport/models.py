from django.db import models
from students.models import Student

class Route(models.Model):
    name = models.CharField(max_length=100)
    stops = models.TextField(help_text="Liste des arrêts séparés par des virgules")
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    number_plate = models.CharField(max_length=20, unique=True)
    capacity = models.PositiveIntegerField()
    driver_name = models.CharField(max_length=100)
    driver_phone = models.CharField(max_length=20)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, related_name='vehicles')

    def __str__(self):
        return f"Bus {self.number_plate} ({self.driver_name})"

class TransportSubscription(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='transport_subscriptions')
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.route.name}"
