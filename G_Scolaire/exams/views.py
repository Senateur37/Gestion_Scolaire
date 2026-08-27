from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Avg
from .models import ExamSession, ExamResult
from academics.models import Course, Enrollment, SchoolClass, Subject
from students.models import Student, Parent


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'ADMIN'

class TeacherOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role in ('TEACHER', 'ADMIN')


# ---------------------------------------------------------------------------
# Sessions d'examen (Admin seulement)
# ---------------------------------------------------------------------------

class SessionListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = ExamSession
    template_name = 'exams/session_list.html'
    context_object_name = 'sessions'
    ordering = ['-start_date']

class SessionCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = ExamSession
    fields = ['name', 'start_date', 'end_date', 'is_active']
    template_name = 'academics/form.html'
    success_url = reverse_lazy('exams:session_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = "Créer une session d'examen"
        return ctx


# ---------------------------------------------------------------------------
# Saisie des notes (Enseignant ou Admin)
# ---------------------------------------------------------------------------

class MarkEntrySelectView(LoginRequiredMixin, TeacherOrAdminMixin, View):
    """Page de sélection : quelle classe + quelle session ?"""

    def get(self, request):
        sessions = ExamSession.objects.filter(is_active=True).order_by('-start_date')

        # Pour un enseignant : uniquement ses classes
        if request.user.role == 'TEACHER':
            teacher = getattr(request.user, 'teacher', None)
            if teacher:
                class_ids = Course.objects.filter(teacher=teacher).values_list('school_class', flat=True).distinct()
                classes = SchoolClass.objects.filter(pk__in=class_ids).order_by('level', 'section')
            else:
                classes = SchoolClass.objects.none()
        else:
            classes = SchoolClass.objects.all().order_by('level', 'section')

        return render(request, 'exams/mark_entry_select.html', {
            'classes': classes,
            'sessions': sessions,
        })


class MarkEntryClassView(LoginRequiredMixin, TeacherOrAdminMixin, View):
    """Tableau de saisie des notes pour tous les élèves d'une classe, par matière."""

    def _get_context(self, request, class_id, session_id):
        school_class = get_object_or_404(SchoolClass, pk=class_id)
        session = get_object_or_404(ExamSession, pk=session_id)

        # Matières enseignées dans cette classe (via courses)
        if request.user.role == 'TEACHER':
            teacher = getattr(request.user, 'teacher', None)
            subjects = Subject.objects.filter(
                course__school_class=school_class,
                course__teacher=teacher
            ).distinct()
        else:
            subjects = Subject.objects.filter(
                course__school_class=school_class
            ).distinct()

        # Élèves inscrits dans la classe, triés par nom
        enrollments = Enrollment.objects.filter(
            school_class=school_class
        ).select_related('student__user').order_by('student__user__last_name')

        students = [e.student for e in enrollments]

        # Récupérer toutes les notes existantes (dict pour accès rapide)
        existing = ExamResult.objects.filter(
            student__in=students,
            subject__in=subjects,
            exam_session=session
        )
        grades_map = {}
        for res in existing:
            grades_map[(res.student_id, res.subject_id)] = res

        return school_class, session, subjects, students, grades_map

    def _build_rows(self, students, subjects, grades_map):
        """Build student rows with cells and averages for the template."""
        rows = []
        for student in students:
            cells = []
            values = []
            for subject in subjects:
                res = grades_map.get((student.id, subject.id))
                val = float(res.marks_obtained) if res else None
                cells.append({'subject': subject, 'value': val})
                if val is not None:
                    values.append(val)
            avg = round(sum(values) / len(values), 2) if values else None
            rows.append({'student': student, 'cells': cells, 'average': avg})
        return rows

    def get(self, request, class_id, session_id):
        school_class, session, subjects, students, grades_map = self._get_context(request, class_id, session_id)
        student_rows = self._build_rows(students, subjects, grades_map)
        return render(request, 'exams/mark_entry_class.html', {
            'school_class': school_class,
            'session': session,
            'subjects': subjects,
            'students': students,
            'grades_map': grades_map,
            'student_rows': student_rows,
        })

    def post(self, request, class_id, session_id):
        school_class, session, subjects, students, grades_map = self._get_context(request, class_id, session_id)

        saved = 0
        for student in students:
            for subject in subjects:
                key = f'mark_{student.id}_{subject.id}'
                remark_key = f'remark_{student.id}_{subject.id}'
                mark_str = request.POST.get(key, '').strip()
                remarks = request.POST.get(remark_key, '').strip()
                if mark_str:
                    try:
                        mark = float(mark_str)
                        if 0 <= mark <= 20:
                            ExamResult.objects.update_or_create(
                                student=student,
                                subject=subject,
                                exam_session=session,
                                defaults={
                                    'marks_obtained': mark,
                                    'total_marks': 20.0,
                                    'remarks': remarks,
                                }
                            )
                            saved += 1
                    except ValueError:
                        pass

        messages.success(request, f"{saved} note(s) enregistrée(s) avec succès.")
        return redirect(request.path)


# ---------------------------------------------------------------------------
# Bulletins de notes
# ---------------------------------------------------------------------------

class BulletinClassSelectView(LoginRequiredMixin, TeacherOrAdminMixin, View):
    """Sélection classe + session pour voir les bulletins."""

    def get(self, request):
        sessions = ExamSession.objects.all().order_by('-start_date')
        if request.user.role == 'TEACHER':
            teacher = getattr(request.user, 'teacher', None)
            if teacher:
                class_ids = Course.objects.filter(teacher=teacher).values_list('school_class', flat=True).distinct()
                classes = SchoolClass.objects.filter(pk__in=class_ids).order_by('level', 'section')
            else:
                classes = SchoolClass.objects.none()
        else:
            classes = SchoolClass.objects.all().order_by('level', 'section')
        return render(request, 'exams/bulletin_select.html', {
            'classes': classes,
            'sessions': sessions,
        })


class BulletinClassView(LoginRequiredMixin, TeacherOrAdminMixin, View):
    """Liste des bulletins de tous les élèves d'une classe pour une session."""

    def get(self, request, class_id, session_id):
        school_class = get_object_or_404(SchoolClass, pk=class_id)
        session = get_object_or_404(ExamSession, pk=session_id)

        enrollments = Enrollment.objects.filter(
            school_class=school_class
        ).select_related('student__user').order_by('student__user__last_name')

        students_summary = []
        for enr in enrollments:
            results = ExamResult.objects.filter(
                student=enr.student,
                exam_session=session
            ).select_related('subject')
            if results.exists():
                avg = sum(r.marks_obtained for r in results) / len(results)
            else:
                avg = None
            students_summary.append({
                'student': enr.student,
                'results_count': results.count(),
                'average': round(avg, 2) if avg is not None else None,
            })

        # Classement par moyenne décroissante
        students_summary.sort(key=lambda x: x['average'] or 0, reverse=True)
        for i, s in enumerate(students_summary):
            s['rank'] = i + 1

        return render(request, 'exams/bulletin_class.html', {
            'school_class': school_class,
            'session': session,
            'students_summary': students_summary,
        })


class BulletinStudentView(LoginRequiredMixin, View):
    """Bulletin individuel d'un élève pour une session. Accessible par Admin, Enseignant, le parent de l'élève ou l'élève lui-même."""

    def get(self, request, student_id, session_id):
        student = get_object_or_404(Student, pk=student_id)
        session = get_object_or_404(ExamSession, pk=session_id)

        # Contrôle des autorisations d'accès
        user = request.user
        if user.role == 'ADMIN' or user.is_superuser:
            pass
        elif user.role == 'TEACHER':
            pass
        elif user.role == 'STUDENT':
            if not hasattr(user, 'student') or user.student.id != student.id:
                messages.error(request, "Vous n'êtes pas autorisé à consulter ce bulletin.")
                return redirect('dashboard')
        elif user.role == 'PARENT':
            if not hasattr(user, 'parent') or student not in user.parent.student_set.all():
                messages.error(request, "Vous n'êtes pas autorisé à consulter le bulletin de cet élève.")
                return redirect('dashboard')
        else:
            messages.error(request, "Accès refusé.")
            return redirect('dashboard')

        results = ExamResult.objects.filter(
            student=student,
            exam_session=session
        ).select_related('subject').order_by('subject__name')

        total = sum(r.marks_obtained for r in results)
        count = results.count()
        average = round(total / count, 2) if count else None

        # Mention
        mention = ''
        if average is not None:
            if average >= 16:
                mention = 'Très Bien'
            elif average >= 14:
                mention = 'Bien'
            elif average >= 12:
                mention = 'Assez Bien'
            elif average >= 10:
                mention = 'Passable'
            else:
                mention = 'Insuffisant'

        # Rang dans la classe
        enrollment = Enrollment.objects.filter(student=student).first()
        rank = None
        class_count = None
        if enrollment:
            class_students = Enrollment.objects.filter(
                school_class=enrollment.school_class
            ).values_list('student', flat=True)
            all_avgs = []
            for sid in class_students:
                res = ExamResult.objects.filter(student_id=sid, exam_session=session)
                if res.exists():
                    avg = sum(r.marks_obtained for r in res) / res.count()
                    all_avgs.append((sid, avg))
            all_avgs.sort(key=lambda x: x[1], reverse=True)
            for i, (sid, avg) in enumerate(all_avgs):
                if sid == student.id:
                    rank = i + 1
            class_count = len(all_avgs)

        return render(request, 'exams/bulletin_student.html', {
            'student': student,
            'session': session,
            'results': results,
            'average': average,
            'mention': mention,
            'rank': rank,
            'class_count': class_count,
            'enrollment': enrollment,
        })


class ParentChildrenBulletinsView(LoginRequiredMixin, View):
    """Page dédiée pour lister et consulter les bulletins des enfants par session (accessible aux parents et aux admins)."""

    def get(self, request):
        if request.user.role not in ('PARENT', 'ADMIN') and not request.user.is_superuser:
            messages.error(request, "Accès non autorisé.")
            return redirect('dashboard')

        sessions = ExamSession.objects.all().order_by('-start_date')
        active_session = ExamSession.objects.filter(is_active=True).first()

        selected_session_id = request.GET.get('session_id')
        if selected_session_id:
            current_session = get_object_or_404(ExamSession, pk=selected_session_id)
        else:
            current_session = active_session or sessions.first()

        all_parents = Parent.objects.select_related('user').all() if request.user.role == 'ADMIN' or request.user.is_superuser else None
        
        if request.user.role == 'PARENT':
            parent = getattr(request.user, 'parent', None)
        else:
            # Admin selecting a parent or defaulting to first parent
            parent_id = request.GET.get('parent_id')
            if parent_id:
                parent = get_object_or_404(Parent, pk=parent_id)
            else:
                parent = all_parents.first() if all_parents else None

        children_bulletins = []
        if parent and current_session:
            children = parent.student_set.all().select_related('user')
            for child in children:
                enrollment = Enrollment.objects.filter(student=child).select_related('school_class').first()
                results = ExamResult.objects.filter(student=child, exam_session=current_session).select_related('subject')
                
                avg = None
                if results.exists():
                    avg = round(sum(r.marks_obtained for r in results) / results.count(), 2)

                mention = ''
                if avg is not None:
                    if avg >= 16:
                        mention = 'Très Bien'
                    elif avg >= 14:
                        mention = 'Bien'
                    elif avg >= 12:
                        mention = 'Assez Bien'
                    elif avg >= 10:
                        mention = 'Passable'
                    else:
                        mention = 'Insuffisant'

                children_bulletins.append({
                    'student': child,
                    'school_class': enrollment.school_class if enrollment else None,
                    'results_count': results.count(),
                    'average': avg,
                    'mention': mention,
                })

        return render(request, 'exams/parent_bulletins.html', {
            'parent': parent,
            'all_parents': all_parents,
            'sessions': sessions,
            'current_session': current_session,
            'children_bulletins': children_bulletins,
        })


class StudentMyBulletinView(LoginRequiredMixin, View):
    """Page pour un élève pour voir tous ses bulletins par session."""

    def get(self, request):
        if request.user.role != 'STUDENT':
            messages.error(request, "Cette page est réservée aux élèves.")
            return redirect('dashboard')

        student = getattr(request.user, 'student', None)
        sessions = ExamSession.objects.all().order_by('-start_date')
        active_session = ExamSession.objects.filter(is_active=True).first()

        selected_session_id = request.GET.get('session_id')
        if selected_session_id:
            current_session = get_object_or_404(ExamSession, pk=selected_session_id)
        else:
            current_session = active_session or sessions.first()

        if not student or not current_session:
            messages.info(request, "Aucun bulletin disponible.")
            return redirect('dashboard')

        return redirect('exams:bulletin_student', student_id=student.pk, session_id=current_session.pk)
