from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Teacher
from .forms import TeacherUserForm, TeacherProfileForm

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'ADMIN'

class TeacherListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Teacher
    template_name = 'teachers/teacher_list.html'
    context_object_name = 'teachers'
    
@login_required
def teacher_create(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
        
    if request.method == 'POST':
        user_form = TeacherUserForm(request.POST)
        profile_form = TeacherProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, f"L'enseignant {user.get_full_name()} a été créé avec succès. Identifiant: {user.username}")
            return redirect('teachers:list')
    else:
        user_form = TeacherUserForm()
        profile_form = TeacherProfileForm()
        
    return render(request, 'teachers/teacher_form.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'action': 'Créer'
    })

@login_required
def teacher_update(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
        
    teacher = get_object_or_404(Teacher, pk=pk)
    
    if request.method == 'POST':
        user_form = TeacherUserForm(request.POST, instance=teacher.user)
        profile_form = TeacherProfileForm(request.POST, instance=teacher)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            if user_form.cleaned_data.get('password'):
                user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile_form.save()
            messages.success(request, "L'enseignant a été mis à jour.")
            return redirect('teachers:list')
    else:
        user_form = TeacherUserForm(instance=teacher.user)
        profile_form = TeacherProfileForm(instance=teacher)
        
    return render(request, 'teachers/teacher_form.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'action': 'Modifier'
    })

class TeacherDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Teacher
    template_name = 'teachers/teacher_confirm_delete.html'
    success_url = reverse_lazy('teachers:list')
    
    def form_valid(self, form):
        teacher = self.get_object()
        user = teacher.user
        response = super().form_valid(form)
        user.delete()
        messages.success(self.request, "L'enseignant a été supprimé.")
        return response
