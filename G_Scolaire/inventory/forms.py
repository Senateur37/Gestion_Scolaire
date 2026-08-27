from django import forms
from .models import Asset, AssetCategory, AssetIssue

class AssetCategoryForm(forms.ModelForm):
    class Meta:
        model = AssetCategory
        fields = ['name']
        labels = {
            'name': 'Nom de la catégorie'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-slate-800/60 border border-slate-600/50 text-white rounded-xl px-4 py-2.5 focus:ring-2 focus:ring-brand-500/50 focus:border-brand-500 outline-none'})
        }

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'category', 'quantity', 'unit_price', 'purchase_date']
        labels = {
            'name': 'Nom du matériel / équipement',
            'category': 'Catégorie',
            'quantity': 'Quantité en stock',
            'unit_price': 'Prix unitaire (€)',
            'purchase_date': "Date d'achat"
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-slate-800/60 border border-slate-600/50 text-white rounded-xl px-4 py-2.5 focus:ring-2 focus:ring-brand-500/50 focus:border-brand-500 outline-none'}),
            'category': forms.Select(attrs={'class': 'w-full bg-slate-800/60 border border-slate-600/50 text-white rounded-xl px-4 py-2.5 focus:ring-2 focus:ring-brand-500/50 focus:border-brand-500 outline-none'}),
            'quantity': forms.NumberInput(attrs={'class': 'w-full bg-slate-800/60 border border-slate-600/50 text-white rounded-xl px-4 py-2.5 focus:ring-2 focus:ring-brand-500/50 focus:border-brand-500 outline-none'}),
            'unit_price': forms.NumberInput(attrs={'class': 'w-full bg-slate-800/60 border border-slate-600/50 text-white rounded-xl px-4 py-2.5 focus:ring-2 focus:ring-brand-500/50 focus:border-brand-500 outline-none'}),
            'purchase_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full bg-slate-800/60 border border-slate-600/50 text-white rounded-xl px-4 py-2.5 focus:ring-2 focus:ring-brand-500/50 focus:border-brand-500 outline-none'}),
        }

class AssetIssueForm(forms.ModelForm):
    class Meta:
        model = AssetIssue
        fields = ['asset', 'issued_to', 'quantity', 'return_date']
        labels = {
            'asset': 'Équipement à attribuer',
            'issued_to': 'Attribué à (Personnel)',
            'quantity': 'Quantité attribuée',
            'return_date': 'Date de retour prévue (optionnel)'
        }
        widgets = {
            'asset': forms.Select(attrs={'class': 'w-full bg-slate-800/60 border border-slate-600/50 text-white rounded-xl px-4 py-2.5 focus:ring-2 focus:ring-brand-500/50 focus:border-brand-500 outline-none'}),
            'issued_to': forms.Select(attrs={'class': 'w-full bg-slate-800/60 border border-slate-600/50 text-white rounded-xl px-4 py-2.5 focus:ring-2 focus:ring-brand-500/50 focus:border-brand-500 outline-none'}),
            'quantity': forms.NumberInput(attrs={'class': 'w-full bg-slate-800/60 border border-slate-600/50 text-white rounded-xl px-4 py-2.5 focus:ring-2 focus:ring-brand-500/50 focus:border-brand-500 outline-none'}),
            'return_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full bg-slate-800/60 border border-slate-600/50 text-white rounded-xl px-4 py-2.5 focus:ring-2 focus:ring-brand-500/50 focus:border-brand-500 outline-none'}),
        }
