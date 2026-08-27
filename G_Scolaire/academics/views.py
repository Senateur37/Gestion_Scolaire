from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SchoolClass, Subject, Enrollment, Course
from .forms import SchoolClassForm, SubjectForm, EnrollmentForm, CourseForm

# --- Classes ---
@login_required
def class_list(request):
    classes = SchoolClass.objects.all()
    return render(request, 'academics/class_list.html', {'classes': classes})

@login_required
def class_create(request):
    if request.method == 'POST':
        form = SchoolClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Classe créée avec succès.')
            return redirect('academics:class_list')
    else:
        form = SchoolClassForm()
    return render(request, 'academics/form.html', {'form': form, 'title': 'Créer une classe'})

@login_required
def class_update(request, pk):
    school_class = get_object_or_404(SchoolClass, pk=pk)
    if request.method == 'POST':
        form = SchoolClassForm(request.POST, instance=school_class)
        if form.is_valid():
            form.save()
            messages.success(request, 'Classe mise à jour.')
            return redirect('academics:class_list')
    else:
        form = SchoolClassForm(instance=school_class)
    return render(request, 'academics/form.html', {'form': form, 'title': 'Modifier la classe'})

@login_required
def class_delete(request, pk):
    school_class = get_object_or_404(SchoolClass, pk=pk)
    if request.method == 'POST':
        school_class.delete()
        messages.success(request, 'Classe supprimée.')
        return redirect('academics:class_list')
    return render(request, 'academics/confirm_delete.html', {'object': school_class, 'title': 'Supprimer la classe'})

# --- Subjects ---
@login_required
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'academics/subject_list.html', {'subjects': subjects})

@login_required
def subject_create(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Matière créée avec succès.')
            return redirect('academics:subject_list')
    else:
        form = SubjectForm()
    return render(request, 'academics/form.html', {'form': form, 'title': 'Créer une matière'})

@login_required
def subject_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Matière mise à jour.')
            return redirect('academics:subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'academics/form.html', {'form': form, 'title': 'Modifier la matière'})

@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Matière supprimée.')
        return redirect('academics:subject_list')
    return render(request, 'academics/confirm_delete.html', {'object': subject, 'title': 'Supprimer la matière'})

# --- Courses (Timetable / Emploi du temps) ---
DAYS_ORDER = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
COURSE_COLORS = [
    '#10b981',  # emerald
    '#3b82f6',  # blue
    '#8b5cf6',  # violet
    '#f59e0b',  # amber
    '#ef4444',  # red
    '#ec4899',  # pink
    '#06b6d4',  # cyan
    '#f97316',  # orange
]

@login_required
def course_list(request):
    classes = SchoolClass.objects.all().order_by('level', 'section')

    class_id = request.GET.get('class_id')
    selected_class = None
    courses_by_day = {day: [] for day in DAYS_ORDER}

    if class_id:
        selected_class = get_object_or_404(SchoolClass, pk=class_id)
        qs = Course.objects.filter(school_class=selected_class).select_related('subject', 'teacher__user').order_by('start_time')
        for idx, course in enumerate(qs):
            course.color = COURSE_COLORS[hash(course.subject.name) % len(COURSE_COLORS)]
            if course.day in courses_by_day:
                courses_by_day[course.day].append(course)
    elif request.user.role == 'STUDENT' and hasattr(request.user, 'student'):
        enrollment = Enrollment.objects.filter(student=request.user.student).first()
        if enrollment:
            selected_class = enrollment.school_class
            qs = Course.objects.filter(school_class=selected_class).select_related('subject', 'teacher__user').order_by('start_time')
            for course in qs:
                course.color = COURSE_COLORS[hash(course.subject.name) % len(COURSE_COLORS)]
                if course.day in courses_by_day:
                    courses_by_day[course.day].append(course)
    elif request.user.role == 'TEACHER' and hasattr(request.user, 'teacher'):
        qs = Course.objects.filter(teacher=request.user.teacher).select_related('subject', 'school_class').order_by('start_time')
        for course in qs:
            course.color = COURSE_COLORS[hash(course.subject.name) % len(COURSE_COLORS)]
            if course.day in courses_by_day:
                courses_by_day[course.day].append(course)

    context = {
        'classes': classes,
        'selected_class': selected_class,
        'courses_by_day_list': list(courses_by_day.items()),
        'days': DAYS_ORDER,
    }
    return render(request, 'academics/course_list.html', context)

@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cours ajouté à l\'emploi du temps.')
            return redirect('academics:course_list')
    else:
        form = CourseForm()
    return render(request, 'academics/form.html', {'form': form, 'title': 'Ajouter un cours'})

@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    class_id = course.school_class.pk
    if request.method == 'POST':
        course.delete()
        messages.success(request, "Cours supprimé de l'emploi du temps.")
        from django.urls import reverse
        return redirect(reverse('academics:course_list') + f'?class_id={class_id}')
    return render(request, 'academics/confirm_delete.html', {'object': course, 'title': 'Supprimer ce cours'})

# --- Enrollments (Inscriptions) ---
@login_required
def enrollment_list(request):
    enrollments = Enrollment.objects.all().select_related('student__user', 'school_class')
    return render(request, 'academics/enrollment_list.html', {'enrollments': enrollments})

@login_required
def enrollment_create(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Élève inscrit dans la classe avec succès.')
            return redirect('academics:enrollment_list')
    else:
        form = EnrollmentForm()
    return render(request, 'academics/form.html', {'form': form, 'title': 'Inscrire un Élève'})

@login_required
def enrollment_delete(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Inscription supprimée.')
        return redirect('academics:enrollment_list')
    return render(request, 'academics/confirm_delete.html', {'object': enrollment, 'title': 'Désinscrire l\'élève'})
