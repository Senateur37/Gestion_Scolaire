from django.db import models
from django.conf import settings

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    # Pour déterminer à qui s'adresse l'annonce
    FOR_TEACHERS = 'TEACHERS'
    FOR_STUDENTS = 'STUDENTS'
    FOR_PARENTS = 'PARENTS'
    FOR_ALL = 'ALL'
    
    AUDIENCE_CHOICES = [
        (FOR_ALL, 'Tous'),
        (FOR_TEACHERS, 'Enseignants'),
        (FOR_STUDENTS, 'Élèves'),
        (FOR_PARENTS, 'Parents'),
    ]
    
    audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES, default=FOR_ALL)

    def __str__(self):
        return self.title
