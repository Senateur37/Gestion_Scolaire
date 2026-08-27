from django.db import models
from django.conf import settings
from .validators import validate_file_extension, validate_file_size

class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/', validators=[validate_file_extension, validate_file_size])
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    # Rôle ciblé
    target_role = models.CharField(max_length=20, choices=[
        ('ALL', 'Tous'),
        ('STUDENT', 'Élèves'),
        ('TEACHER', 'Enseignants'),
        ('PARENT', 'Parents')
    ], default='ALL')

    def __str__(self):
        return self.title
