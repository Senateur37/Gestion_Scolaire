from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Attendance
from academics.models import SchoolClass, Enrollment
from students.models import Student

@login_required
def attendance_list(request):
    # Fetch recent attendances that are ABSENT or LATE
    attendances = Attendance.objects.filter(status__in=[Attendance.Status.ABSENT, Attendance.Status.LATE]).order_by('-date', 'student__user__last_name')
    return render(request, 'attendance/attendance_list.html', {'attendances': attendances})

@login_required
def take_attendance(request):
    classes = SchoolClass.objects.all().order_by('level', 'section')
    
    selected_class_id = request.GET.get('class_id') or request.POST.get('class_id')
    selected_date = request.GET.get('date') or request.POST.get('date') or timezone.now().date().isoformat()
    
    selected_class = None
    students_data = []
    
    if selected_class_id:
        selected_class = get_object_or_404(SchoolClass, id=selected_class_id)
        enrollments = Enrollment.objects.filter(school_class=selected_class).select_related('student__user')
        
        # Build student data
        for enrollment in enrollments:
            student = enrollment.student
            # Try to get existing attendance
            att = Attendance.objects.filter(student=student, date=selected_date).first()
            students_data.append({
                'student': student,
                'status': att.status if att else Attendance.Status.PRESENT,
                'justification': att.justification if att else ''
            })
            
    if request.method == 'POST' and selected_class:
        for data in students_data:
            student = data['student']
            status_val = request.POST.get(f'status_{student.id}')
            justif_val = request.POST.get(f'justification_{student.id}', '')
            
            if status_val:
                Attendance.objects.update_or_create(
                    student=student,
                    date=selected_date,
                    defaults={'status': status_val, 'justification': justif_val}
                )
                
        messages.success(request, f"Les présences pour la classe {selected_class} ont été enregistrées avec succès.")
        return redirect('attendance:list')

    return render(request, 'attendance/take_attendance.html', {
        'classes': classes,
        'selected_class': selected_class,
        'selected_date': selected_date,
        'students_data': students_data,
    })
