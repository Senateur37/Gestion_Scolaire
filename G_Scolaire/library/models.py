from django.db import models
from students.models import Student
from accounts.models import User

class BookCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, unique=True)
    category = models.ForeignKey(BookCategory, on_delete=models.SET_NULL, null=True, related_name='books')
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    location = models.CharField(max_length=100, help_text="Ex: Rayon A, Étagère 3")

    def __str__(self):
        return self.title

class BorrowRecord(models.Model):
    class Status(models.TextChoices):
        BORROWED = "BORROWED", "Emprunté"
        RETURNED = "RETURNED", "Retourné"
        OVERDUE = "OVERDUE", "En retard"

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_records')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_books')
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.BORROWED)

    def __str__(self):
        return f"{self.book.title} emprunté par {self.user.get_full_name()}"
