from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    # Sessions d'examen (Admin)
    path('sessions/', views.SessionListView.as_view(), name='session_list'),
    path('sessions/create/', views.SessionCreateView.as_view(), name='session_create'),

    # Saisie des notes (Enseignant / Admin)
    path('marks/select/', views.MarkEntrySelectView.as_view(), name='mark_entry_select'),
    path('marks/class/<int:class_id>/session/<int:session_id>/', views.MarkEntryClassView.as_view(), name='mark_entry_class'),

    # Bulletins (Admin + Enseignant)
    path('bulletins/', views.BulletinClassSelectView.as_view(), name='bulletin_select'),
    path('bulletins/class/<int:class_id>/session/<int:session_id>/', views.BulletinClassView.as_view(), name='bulletin_class'),
    path('bulletins/student/<int:student_id>/session/<int:session_id>/', views.BulletinStudentView.as_view(), name='bulletin_student'),
    
    # Espace dédié Parents & Élèves
    path('bulletins/parent/', views.ParentChildrenBulletinsView.as_view(), name='parent_bulletins'),
    path('bulletins/my-bulletin/', views.StudentMyBulletinView.as_view(), name='student_my_bulletin'),
]
