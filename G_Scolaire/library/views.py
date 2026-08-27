from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Book, BorrowRecord
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'ADMIN'

# --- Books ---
class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'library/book_list.html'
    context_object_name = 'books'

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'category', 'total_copies', 'available_copies', 'location']
        labels = {
            'title': 'Titre',
            'author': 'Auteur',
            'isbn': 'Code ISBN',
            'category': 'Catégorie',
            'total_copies': 'Copies totales',
            'available_copies': 'Copies disponibles',
            'location': 'Emplacement',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sauvegarder', css_class='w-full bg-brand-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-brand-500 transition-colors mt-4'))

class BookCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'academics/form.html'
    success_url = reverse_lazy('library:book_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Ajouter un Livre"
        return context

class BookUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'academics/form.html'
    success_url = reverse_lazy('library:book_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modifier le Livre"
        return context

class BookDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Book
    template_name = 'academics/confirm_delete.html'
    success_url = reverse_lazy('library:book_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Supprimer le Livre"
        return context

# --- Borrows ---
class BorrowListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = BorrowRecord
    template_name = 'library/borrow_list.html'
    context_object_name = 'borrows'

class BorrowForm(forms.ModelForm):
    class Meta:
        model = BorrowRecord
        fields = ['book', 'user', 'due_date', 'return_date', 'status']
        labels = {
            'book': 'Livre',
            'user': 'Emprunteur',
            'due_date': 'Date d\'échéance',
            'return_date': 'Date de retour',
            'status': 'Statut',
        }
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sauvegarder', css_class='w-full bg-brand-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-brand-500 transition-colors mt-4'))

class BorrowCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = BorrowRecord
    form_class = BorrowForm
    template_name = 'academics/form.html'
    success_url = reverse_lazy('library:borrow_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Enregistrer un Emprunt"
        return context

class BorrowUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = BorrowRecord
    form_class = BorrowForm
    template_name = 'academics/form.html'
    success_url = reverse_lazy('library:borrow_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modifier l'Emprunt"
        return context
