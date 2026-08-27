from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Hostel, Room, RoomAllocation
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'ADMIN'

class GenericForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sauvegarder', css_class='w-full bg-brand-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-brand-500 transition-colors mt-4'))

# --- Hostel ---
class HostelListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Hostel
    template_name = 'hostel/hostel_list.html'
    context_object_name = 'hostels'

class HostelForm(GenericForm):
    class Meta:
        model = Hostel
        fields = '__all__'
        labels = {
            'name': 'Nom du Bâtiment / Dortoir',
            'type': 'Type de dortoir',
            'address': 'Adresse',
            'manager': 'Nom du responsable',
        }

class HostelCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Hostel
    form_class = HostelForm
    template_name = 'academics/form.html'
    success_url = reverse_lazy('hostel:hostel_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Ajouter un Bâtiment/Dortoir"
        return context

class HostelUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Hostel
    form_class = HostelForm
    template_name = 'academics/form.html'
    success_url = reverse_lazy('hostel:hostel_list')

class HostelDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Hostel
    template_name = 'academics/confirm_delete.html'
    success_url = reverse_lazy('hostel:hostel_list')

# --- Room ---
class RoomListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Room
    template_name = 'hostel/room_list.html'
    context_object_name = 'rooms'

class RoomForm(GenericForm):
    class Meta:
        model = Room
        fields = '__all__'
        labels = {
            'hostel': 'Bâtiment',
            'room_number': 'Numéro de la chambre',
            'capacity': 'Capacité (Nombre de lits)',
            'cost_per_term': 'Coût par trimestre (€)',
        }

class RoomCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'academics/form.html'
    success_url = reverse_lazy('hostel:room_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Ajouter une Chambre"
        return context

class RoomUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'academics/form.html'
    success_url = reverse_lazy('hostel:room_list')

class RoomDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Room
    template_name = 'academics/confirm_delete.html'
    success_url = reverse_lazy('hostel:room_list')
