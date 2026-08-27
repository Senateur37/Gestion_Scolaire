from django import forms
from .models import ExamResult, ExamSession
from academics.models import Course
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class MarkEntrySelectForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.none(),
        label="Sélectionnez un de vos cours",
        empty_label="--- Choisir un cours ---"
    )
    exam_session = forms.ModelChoiceField(
        queryset=ExamSession.objects.filter(is_active=True),
        label="Session d'Examen",
        empty_label="--- Choisir une session ---"
    )

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields['course'].queryset = Course.objects.filter(teacher=teacher)
        
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Continuer', css_class='w-full bg-brand-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-brand-500 mt-4'))
