from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Announcement

@login_required
def announcement_list(request):
    # Admin sees all; others see what's targeted to them
    if request.user.role == 'ADMIN':
        announcements = Announcement.objects.all().order_by('-date_created')
    elif request.user.role == 'TEACHER':
        announcements = Announcement.objects.filter(
            audience__in=['ALL', 'TEACHERS']
        ).order_by('-date_created')
    elif request.user.role == 'STUDENT':
        announcements = Announcement.objects.filter(
            audience__in=['ALL', 'STUDENTS']
        ).order_by('-date_created')
    elif request.user.role == 'PARENT':
        announcements = Announcement.objects.filter(
            audience__in=['ALL', 'PARENTS']
        ).order_by('-date_created')
    else:
        announcements = Announcement.objects.filter(audience='ALL').order_by('-date_created')

    return render(request, 'communication/announcement_list.html', {
        'announcements': announcements,
    })

@login_required
def announcement_create(request):
    if request.user.role != 'ADMIN':
        return redirect('communication:announcement_list')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        audience = request.POST.get('audience', 'ALL')
        if title and content:
            Announcement.objects.create(
                title=title,
                content=content,
                audience=audience,
                author=request.user,
            )
            messages.success(request, "Annonce publiée avec succès.")
            return redirect('communication:announcement_list')
        else:
            messages.error(request, "Titre et contenu sont obligatoires.")

    audience_choices = Announcement.AUDIENCE_CHOICES
    return render(request, 'communication/announcement_form.html', {
        'audience_choices': audience_choices,
    })

@login_required
def announcement_delete(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('communication:announcement_list')
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        announcement.delete()
        messages.success(request, "Annonce supprimée.")
        return redirect('communication:announcement_list')
    return render(request, 'communication/announcement_confirm_delete.html', {
        'announcement': announcement
    })
