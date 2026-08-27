from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    path('', views.TeacherListView.as_view(), name='list'),
    path('create/', views.teacher_create, name='create'),
    path('<int:pk>/update/', views.teacher_update, name='update'),
    path('<int:pk>/delete/', views.TeacherDeleteView.as_view(), name='delete'),
]
