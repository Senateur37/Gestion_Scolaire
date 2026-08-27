from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Route, Vehicle, TransportSubscription
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'ADMIN'

# --- Generic Form ---
class GenericForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sauvegarder', css_class='w-full bg-brand-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-brand-500 transition-colors mt-4'))

# --- Route ---
class RouteListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Route
    template_name = 'transport/route_list.html'
    context_object_name = 'routes'

class RouteForm(GenericForm):
    class Meta:
        model = Route
        fields = '__all__'
        labels = {
            'name': 'Nom de l\'itinéraire',
            'stops': 'Arrêts (séparés par des virgules)',
            'fee': 'Frais mensuels/annuels (€)',
        }

class RouteCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Route
    form_class = RouteForm
    template_name = 'academics/form.html'
    success_url = reverse_lazy('transport:route_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Créer un Itinéraire"
        return context

class RouteUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Route
    form_class = RouteForm
    template_name = 'academics/form.html'
    success_url = reverse_lazy('transport:route_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modifier l'Itinéraire"
        return context

class RouteDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Route
    template_name = 'academics/confirm_delete.html'
    success_url = reverse_lazy('transport:route_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Supprimer l'Itinéraire"
        return context

# --- Vehicle ---
class VehicleListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Vehicle
    template_name = 'transport/vehicle_list.html'
    context_object_name = 'vehicles'

class VehicleForm(GenericForm):
    class Meta:
        model = Vehicle
        fields = '__all__'
        labels = {
            'number_plate': 'Plaque d\'immatriculation',
            'capacity': 'Capacité (Nombre de places)',
            'driver_name': 'Nom du chauffeur',
            'driver_phone': 'Téléphone du chauffeur',
            'route': 'Itinéraire assigné',
        }

class VehicleCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'academics/form.html'
    success_url = reverse_lazy('transport:vehicle_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Enregistrer un Véhicule"
        return context

class VehicleUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'academics/form.html'
    success_url = reverse_lazy('transport:vehicle_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modifier le Véhicule"
        return context

class VehicleDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Vehicle
    template_name = 'academics/confirm_delete.html'
    success_url = reverse_lazy('transport:vehicle_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Supprimer le Véhicule"
        return context
