from django.db import models
from students.models import Student

class Hostel(models.Model):
    class HostelType(models.TextChoices):
        BOYS = "BOYS", "Garçons"
        GIRLS = "GIRLS", "Filles"
        MIXED = "MIXED", "Mixte"

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=HostelType.choices)
    address = models.TextField(blank=True)
    manager = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20)
    capacity = models.PositiveIntegerField(default=1)
    cost_per_term = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.room_number} ({self.hostel.name})"

class RoomAllocation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='room_allocations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    allocation_date = models.DateField(auto_now_add=True)
    vacation_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} -> {self.room}"
