from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Staff, LeaveRequest, Payroll
from .forms import StaffForm, LeaveRequestForm
from datetime import date

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'ADMIN'

# --- Staff Views ---
class StaffListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Staff
    template_name = 'hr/staff_list.html'
    context_object_name = 'staff_members'

class StaffCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Staff
    form_class = StaffForm
    template_name = 'academics/form.html'
    success_url = reverse_lazy('hr:staff_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Ajouter un membre du personnel"
        return context

class StaffUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Staff
    form_class = StaffForm
    template_name = 'academics/form.html'
    success_url = reverse_lazy('hr:staff_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modifier le personnel"
        return context

class StaffDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Staff
    template_name = 'academics/confirm_delete.html'
    success_url = reverse_lazy('hr:staff_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Supprimer ce membre"
        return context

# --- Leave Views ---
class LeaveListView(LoginRequiredMixin, ListView):
    model = LeaveRequest
    template_name = 'hr/leave_list.html'
    context_object_name = 'leaves'
    
    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return LeaveRequest.objects.all().order_by('-start_date')
        elif hasattr(self.request.user, 'staff_profile'):
            return LeaveRequest.objects.filter(staff=self.request.user.staff_profile).order_by('-start_date')
        return LeaveRequest.objects.none()

class LeaveCreateView(LoginRequiredMixin, CreateView):
    model = LeaveRequest
    form_class = LeaveRequestForm
    template_name = 'academics/form.html'
    success_url = reverse_lazy('hr:leave_list')
    
    def form_valid(self, form):
        if not hasattr(self.request.user, 'staff_profile'):
            messages.error(self.request, "Vous n'avez pas de profil de personnel associé.")
            return redirect('hr:leave_list')
        form.instance.staff = self.request.user.staff_profile
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Demander un congé"
        return context

@user_passes_test(lambda u: u.role == 'ADMIN')
def approve_leave(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    leave.status = LeaveRequest.Status.APPROVED
    leave.save()
    messages.success(request, "Congé approuvé.")
    return redirect('hr:leave_list')

@user_passes_test(lambda u: u.role == 'ADMIN')
def reject_leave(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    leave.status = LeaveRequest.Status.REJECTED
    leave.save()
    messages.warning(request, "Congé refusé.")
    return redirect('hr:leave_list')

# --- Payroll Views ---
class PayrollListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Payroll
    template_name = 'hr/payroll_list.html'
    context_object_name = 'payrolls'
    ordering = ['-month', 'staff__user__last_name']

@user_passes_test(lambda u: u.role == 'ADMIN')
def generate_payroll(request):
    if request.method == 'POST':
        month_str = request.POST.get('month')
        if month_str:
            # Parse 'YYYY-MM'
            year, month = map(int, month_str.split('-'))
            payroll_date = date(year, month, 1)
            
            staff_members = Staff.objects.all()
            generated = 0
            for staff in staff_members:
                _, created = Payroll.objects.get_or_create(
                    staff=staff,
                    month=payroll_date,
                    defaults={'net_salary': staff.basic_salary}
                )
                if created:
                    generated += 1
                    
            messages.success(request, f"{generated} fiches de paie générées pour {month_str}.")
            return redirect('hr:payroll_list')
            
    return render(request, 'hr/generate_payroll.html')

@user_passes_test(lambda u: u.role == 'ADMIN')
def mark_paid(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)
    payroll.is_paid = True
    payroll.payment_date = timezone.now().date()
    payroll.save()
    messages.success(request, f"Paie de {payroll.staff} marquée comme réglée.")
    return redirect('hr:payroll_list')
