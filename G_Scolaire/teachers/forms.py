from django import forms
from django.contrib.auth import get_user_model
from .models import Teacher

User = get_user_model()

class TeacherUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False, help_text="Laissez vide pour générer automatiquement")
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom de famille',
            'email': 'Adresse E-mail',
            'phone': 'Numéro de téléphone',
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'TEACHER'
        
        # Générer un username si non fourni
        if not user.username:
            base_username = f"prof.{user.last_name.lower()}".replace(" ", "")
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            user.username = username
            
        if commit:
            if self.cleaned_data.get('password'):
                user.set_password(self.cleaned_data['password'])
            else:
                user.set_password('password123')
            user.save()
        return user


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['employee_number', 'specialization', 'neighborhood']
        labels = {
            'employee_number': 'Numéro d\'employé',
            'specialization': 'Spécialisation',
            'neighborhood': 'Quartier',
        }
