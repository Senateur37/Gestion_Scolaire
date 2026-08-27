from django import forms
from .models import SchoolClass, Subject, Enrollment, Course
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class GenericForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sauvegarder', css_class='w-full bg-brand-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-brand-500 transition-colors mt-4'))

class SchoolClassForm(GenericForm):
    class Meta:
        model = SchoolClass
        fields = ['level', 'section', 'name', 'academic_year', 'main_teacher']
        labels = {
            'level': 'Niveau scolaire (Année 1-12)',
            'section': 'Section / Groupe (ex: A, B, C)',
            'name': 'Nom complet personnalisé (Optionnel)',
            'academic_year': 'Année académique',
            'main_teacher': 'Professeur principal',
        }

class SubjectForm(GenericForm):
    class Meta:
        model = Subject
        fields = ['name', 'code']
        labels = {
            'name': 'Matière',
            'code': 'Code',
        }

class EnrollmentForm(GenericForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'school_class']
        labels = {
            'student': 'Élève',
            'school_class': 'Classe',
        }

class CourseForm(GenericForm):
    class Meta:
        model = Course
        fields = ['school_class', 'subject', 'teacher', 'day', 'start_time', 'end_time', 'room']
        labels = {
            'school_class': 'Classe',
            'subject': 'Matière',
            'teacher': 'Enseignant',
            'day': 'Jour',
            'start_time': 'Heure de début',
            'end_time': 'Heure de fin',
            'room': 'Salle',
        }
        widgets = {
            'start_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'end_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }
