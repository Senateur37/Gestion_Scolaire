from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Student, Parent
from .forms import StudentUserForm, StudentProfileForm, ParentUserForm, ParentProfileForm

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.role == 'ADMIN' or self.request.user.is_superuser)


# ==============================================================================
# ÉLÈVES (STUDENTS)
# ==============================================================================
class StudentListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    
@login_required
def student_create(request):
    if request.user.role != 'ADMIN' and not request.user.is_superuser:
        return redirect('dashboard')
        
    if request.method == 'POST':
        user_form = StudentUserForm(request.POST)
        profile_form = StudentProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            profile_form.save_m2m()
            messages.success(request, f"L'élève {user.get_full_name()} a été créé avec succès. Identifiant: {user.username}")
            return redirect('students:list')
    else:
        user_form = StudentUserForm()
        profile_form = StudentProfileForm()
        
    return render(request, 'students/student_form.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'action': 'Créer'
    })

@login_required
def student_update(request, pk):
    if request.user.role != 'ADMIN' and not request.user.is_superuser:
        return redirect('dashboard')
        
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        user_form = StudentUserForm(request.POST, instance=student.user)
        profile_form = StudentProfileForm(request.POST, instance=student)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            if user_form.cleaned_data.get('password'):
                user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile_form.save()
            messages.success(request, "L'élève a été mis à jour.")
            return redirect('students:list')
    else:
        user_form = StudentUserForm(instance=student.user)
        profile_form = StudentProfileForm(instance=student)
        
    return render(request, 'students/student_form.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'action': 'Modifier'
    })

class StudentDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('students:list')
    
    def form_valid(self, form):
        student = self.get_object()
        user = student.user
        response = super().form_valid(form)
        user.delete()
        messages.success(self.request, "L'élève a été supprimé.")
        return response


# ==============================================================================
# PARENTS D'ÉLÈVES
# ==============================================================================
class ParentListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Parent
    template_name = 'students/parent_list.html'
    context_object_name = 'parents'

    def get_queryset(self):
        return Parent.objects.select_related('user').prefetch_related('student_set__user').order_by('user__last_name')


@login_required
def parent_create(request):
    if request.user.role != 'ADMIN' and not request.user.is_superuser:
        return redirect('dashboard')

    if request.method == 'POST':
        user_form = ParentUserForm(request.POST)
        profile_form = ParentProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            parent = profile_form.save(commit=False)
            parent.user = user
            parent.save()

            # Lier les enfants sélectionnés
            selected_children = profile_form.cleaned_data.get('children', [])
            for child in selected_children:
                child.parents.add(parent)

            messages.success(request, f"Le parent {user.get_full_name()} a été créé avec succès. Identifiant: {user.username} (Mot de passe: password123)")
            return redirect('students:parent_list')
    else:
        user_form = ParentUserForm()
        profile_form = ParentProfileForm()

    return render(request, 'students/parent_form.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'action': 'Créer'
    })


@login_required
def parent_update(request, pk):
    if request.user.role != 'ADMIN' and not request.user.is_superuser:
        return redirect('dashboard')

    parent = get_object_or_404(Parent, pk=pk)

    if request.method == 'POST':
        user_form = ParentUserForm(request.POST, instance=parent.user)
        profile_form = ParentProfileForm(request.POST, instance=parent)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            if user_form.cleaned_data.get('password'):
                user.set_password(user_form.cleaned_data['password'])
            user.save()
            parent = profile_form.save()

            # Mettre à jour les liens enfants
            selected_children = profile_form.cleaned_data.get('children', [])
            parent.student_set.set(selected_children)

            messages.success(request, f"Le parent {user.get_full_name()} a été mis à jour.")
            return redirect('students:parent_list')
    else:
        user_form = ParentUserForm(instance=parent.user)
        profile_form = ParentProfileForm(instance=parent)

    return render(request, 'students/parent_form.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'action': 'Modifier'
    })


class ParentDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Parent
    template_name = 'academics/confirm_delete.html'
    success_url = reverse_lazy('students:parent_list')

    def form_valid(self, form):
        parent = self.get_object()
        user = parent.user
        response = super().form_valid(form)
        user.delete()
        messages.success(self.request, "Le parent a été supprimé.")
        return response
