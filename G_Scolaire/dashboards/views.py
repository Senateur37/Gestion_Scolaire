from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg
from django.utils import timezone
import json

from students.models import Student, Parent
from teachers.models import Teacher
from academics.models import SchoolClass, Enrollment, Course
from attendance.models import Attendance
from payments.models import Payment
from communication.models import Announcement
from exams.models import ExamSession, ExamResult
from hr.models import Staff, Payroll, LeaveRequest


@login_required
def dashboard_router(request):
    role = request.user.role
    if role == 'ADMIN':
        return redirect('admin_dashboard')
    elif role == 'TEACHER':
        return redirect('teacher_dashboard')
    elif role == 'STUDENT':
        return redirect('student_dashboard')
    elif role == 'PARENT':
        return redirect('parent_dashboard')
    return redirect('admin_dashboard')


# ==============================================================================
# 1. TABLEAU DE BORD ADMINISTRATEUR
# ==============================================================================
@login_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN' and not request.user.is_superuser:
        return redirect('dashboard')

    # --- KPIs principaux ---
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_classes = SchoolClass.objects.count()
    
    today = timezone.now().date()
    month_start = today.replace(day=1)
    total_absences = Attendance.objects.filter(status='ABSENT', date__gte=month_start).count()
    
    # Finances
    total_collected = Payment.objects.aggregate(s=Sum('amount_paid'))['s'] or 0
    total_expected = Payment.objects.aggregate(s=Sum('amount'))['s'] or 0
    remaining_due = max(0, float(total_expected) - float(total_collected))

    # --- KPIs RH ---
    total_staff = Staff.objects.count()
    pending_payroll_amount = Payroll.objects.filter(is_paid=False).aggregate(s=Sum('net_salary'))['s'] or 0
    pending_leaves = LeaveRequest.objects.filter(status='PENDING').count()

    # --- Données graphique Effectifs par classe (réelles) ---
    classes_qs = SchoolClass.objects.annotate(nb=Count('enrollment')).order_by('level', 'section')
    class_names = json.dumps([f"{c.level}e {c.section}" if c.section else f"Cl. {c.level}" for c in classes_qs])
    class_counts = json.dumps([c.nb for c in classes_qs])

    # --- Données graphique Paiements (réelles) ---
    finance_data = json.dumps([float(total_collected), float(remaining_due)])

    # Dernières activités
    recent_payments = Payment.objects.select_related('student__user').order_by('-id')[:5]
    recent_absences = Attendance.objects.filter(status='ABSENT').select_related('student__user').order_by('-date')[:5]

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_classes': total_classes,
        'total_absences': total_absences,
        'total_collected': total_collected,
        'total_expected': total_expected,
        'remaining_due': remaining_due,
        'total_staff': total_staff,
        'pending_payroll_amount': pending_payroll_amount,
        'pending_leaves': pending_leaves,
        'class_names': class_names,
        'class_counts': class_counts,
        'finance_data': finance_data,
        'recent_payments': recent_payments,
        'recent_absences': recent_absences,
    }
    return render(request, 'dashboards/admin_dashboard.html', context)


# ==============================================================================
# 2. TABLEAU DE BORD ENSEIGNANT
# ==============================================================================
@login_required
def teacher_dashboard(request):
    if request.user.role != 'TEACHER':
        return redirect('dashboard')

    teacher = getattr(request.user, 'teacher', None)
    assigned_classes = []
    courses = []
    total_students_taught = 0
    active_session = ExamSession.objects.filter(is_active=True).first()

    if teacher:
        # Classes où il est prof principal OU donne des cours
        main_cls = SchoolClass.objects.filter(main_teacher=teacher)
        course_cls = SchoolClass.objects.filter(course__teacher=teacher)
        assigned_classes = (main_cls | course_cls).distinct().annotate(student_count=Count('enrollment')).order_by('level', 'section')
        
        # Cours de l'enseignant
        courses = Course.objects.filter(teacher=teacher).select_related('school_class', 'subject').order_by('day', 'start_time')
        
        # Nombre total d'élèves uniques auxquels il enseigne
        taught_class_ids = assigned_classes.values_list('id', flat=True)
        total_students_taught = Enrollment.objects.filter(school_class_id__in=taught_class_ids).values('student').distinct().count()

    announcements = Announcement.objects.filter(audience__in=['ALL', 'TEACHERS']).order_by('-date_created')[:4]

    context = {
        'teacher': teacher,
        'assigned_classes': assigned_classes,
        'courses': courses,
        'total_students_taught': total_students_taught,
        'active_session': active_session,
        'announcements': announcements,
    }
    return render(request, 'dashboards/teacher_dashboard.html', context)


# ==============================================================================
# 3. TABLEAU DE BORD ÉLÈVE
# ==============================================================================
@login_required
def student_dashboard(request):
    if request.user.role != 'STUDENT':
        return redirect('dashboard')

    student = getattr(request.user, 'student', None)
    school_class = None
    recent_grades = []
    overall_average = None
    absences_count = 0
    late_count = 0
    recent_attendances = []
    timetable = []
    payments = []
    active_session = ExamSession.objects.filter(is_active=True).first()

    if student:
        # Classe actuelle
        enrollment = Enrollment.objects.filter(student=student).select_related('school_class').first()
        if enrollment:
            school_class = enrollment.school_class
            # Emploi du temps de sa classe
            timetable = Course.objects.filter(school_class=school_class).select_related('subject', 'teacher__user').order_by('day', 'start_time')

        # Notes et résultats
        recent_grades = ExamResult.objects.filter(student=student).select_related('subject', 'exam_session').order_by('-id')[:6]
        
        if active_session:
            session_grades = ExamResult.objects.filter(student=student, exam_session=active_session)
            if session_grades.exists():
                overall_average = round(session_grades.aggregate(avg=Avg('marks_obtained'))['avg'] or 0, 2)

        # Absences & Retards
        absences_count = Attendance.objects.filter(student=student, status='ABSENT').count()
        late_count = Attendance.objects.filter(student=student, status='LATE').count()
        recent_attendances = Attendance.objects.filter(student=student).order_by('-date')[:5]

        # Paiements
        payments = Payment.objects.filter(student=student).order_by('-due_date')

    announcements = Announcement.objects.filter(audience__in=['ALL', 'STUDENTS']).order_by('-date_created')[:4]

    context = {
        'student': student,
        'school_class': school_class,
        'recent_grades': recent_grades,
        'overall_average': overall_average,
        'absences_count': absences_count,
        'late_count': late_count,
        'recent_attendances': recent_attendances,
        'timetable': timetable,
        'payments': payments,
        'active_session': active_session,
        'announcements': announcements,
    }
    return render(request, 'dashboards/student_dashboard.html', context)


# ==============================================================================
# 4. TABLEAU DE BORD PARENT
# ==============================================================================
@login_required
def parent_dashboard(request):
    if request.user.role != 'PARENT':
        return redirect('dashboard')

    parent = getattr(request.user, 'parent', None)
    children_data = []
    active_session = ExamSession.objects.filter(is_active=True).first()

    if parent:
        children = parent.student_set.all().select_related('user')
        for child in children:
            enrollment = Enrollment.objects.filter(student=child).select_related('school_class').first()
            school_class = enrollment.school_class if enrollment else None
            
            # Notes & Moyenne
            grades = ExamResult.objects.filter(student=child).select_related('subject', 'exam_session').order_by('-id')[:5]
            avg = None
            if active_session:
                res = ExamResult.objects.filter(student=child, exam_session=active_session)
                if res.exists():
                    avg = round(res.aggregate(a=Avg('marks_obtained'))['a'] or 0, 2)

            # Absences
            absences = Attendance.objects.filter(student=child, status='ABSENT').count()
            lates = Attendance.objects.filter(student=child, status='LATE').count()
            recent_abs = Attendance.objects.filter(student=child).order_by('-date')[:4]

            # Paiements
            payments = Payment.objects.filter(student=child).order_by('-due_date')
            total_due = payments.aggregate(s=Sum('amount'))['s'] or 0
            total_paid = payments.aggregate(s=Sum('amount_paid'))['s'] or 0
            remaining = max(0, float(total_due) - float(total_paid))

            children_data.append({
                'student': child,
                'school_class': school_class,
                'grades': grades,
                'average': avg,
                'absences_count': absences,
                'late_count': lates,
                'recent_attendances': recent_abs,
                'payments': payments,
                'total_due': total_due,
                'total_paid': total_paid,
                'remaining': remaining,
            })

    announcements = Announcement.objects.filter(audience__in=['ALL', 'PARENTS']).order_by('-date_created')[:5]

    context = {
        'parent': parent,
        'children_data': children_data,
        'active_session': active_session,
        'announcements': announcements,
    }
    return render(request, 'dashboards/parent_dashboard.html', context)
