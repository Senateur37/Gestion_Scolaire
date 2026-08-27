from django import forms
from .models import Staff, LeaveRequest, Payroll
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['user', 'department', 'designation', 'date_of_joining', 'basic_salary']
        labels = {
            'user': 'Utilisateur',
            'department': 'Département',
            'designation': 'Poste / Titre',
            'date_of_joining': 'Date d\'embauche',
            'basic_salary': 'Salaire de base (FCFA)',
        }
        widgets = {
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.fields['user'].queryset = User.objects.filter(role='ADMIN')
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Enregistrer', css_class='w-full bg-brand-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-brand-500 transition-colors mt-4'))

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date', 'reason']
        labels = {
            'start_date': 'Date de début',
            'end_date': 'Date de fin',
            'reason': 'Motif du congé',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Soumettre la demande', css_class='w-full bg-brand-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-brand-500 transition-colors mt-4'))
