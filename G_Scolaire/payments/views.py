from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Payment
from .forms import PaymentForm

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'ADMIN'

class PaymentListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Payment
    template_name = 'payments/payment_list.html'
    context_object_name = 'payments'
    ordering = ['-due_date']

class PaymentCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'academics/form.html'  # Reusing the generic crispy-tailwind form template
    success_url = reverse_lazy('payments:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Enregistrer un Paiement"
        return context

class PaymentUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'academics/form.html'
    success_url = reverse_lazy('payments:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modifier le Paiement"
        return context

class PaymentDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Payment
    template_name = 'academics/confirm_delete.html'
    success_url = reverse_lazy('payments:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Supprimer le paiement"
        return context
