from django import forms
from .models import Payment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student', 'amount', 'amount_paid', 'due_date', 'payment_date', 'description']
        labels = {
            'student': 'Élève',
            'amount': 'Montant Total Dû',
            'amount_paid': 'Montant Déjà Versé',
            'due_date': 'Date d\'échéance',
            'payment_date': 'Date du dernier versement',
            'description': 'Motif / Description (ex: Scolarité Annuelle)',
        }
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Enregistrer le paiement', css_class='w-full bg-brand-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-brand-500 transition-colors mt-4'))
