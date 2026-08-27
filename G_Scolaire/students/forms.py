from django import forms
from django.contrib.auth import get_user_model
from .models import Student, Parent

User = get_user_model()

class StudentUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False, help_text="Laissez vide pour générer un mot de passe par défaut (password123)")
    
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
        user.role = 'STUDENT'
        
        if not user.username:
            base_username = f"{user.first_name.lower()}.{user.last_name.lower()}".replace(" ", "")
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


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['parents', 'gender', 'birth_date', 'age', 'neighborhood', 'parent_contact', 'address', 'registration_number']
        labels = {
            'parents': 'Parents / Tuteurs rattachés',
            'gender': 'Sexe',
            'birth_date': 'Date de naissance',
            'age': 'Âge',
            'neighborhood': 'Quartier',
            'parent_contact': 'Numéro du parent / Tuteur',
            'address': 'Adresse',
            'registration_number': 'Matricule',
        }
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }


class ParentUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False, help_text="Laissez vide pour générer un mot de passe par défaut (password123)")

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
        user.role = 'PARENT'

        if not user.username:
            base_username = f"parent.{user.first_name.lower()}.{user.last_name.lower()}".replace(" ", "")
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


class ParentProfileForm(forms.ModelForm):
    children = forms.ModelMultipleChoiceField(
        queryset=Student.objects.select_related('user').all(),
        required=False,
        label="Enfant(s) rattaché(s)",
        help_text="Sélectionnez les élèves rattachés à ce parent"
    )

    class Meta:
        model = Parent
        fields = ['address']
        labels = {
            'address': 'Adresse de résidence',
        }
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['children'].initial = self.instance.student_set.all()
