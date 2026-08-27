from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    # Élèves
    path('', views.StudentListView.as_view(), name='list'),
    path('create/', views.student_create, name='create'),
    path('<int:pk>/update/', views.student_update, name='update'),
    path('<int:pk>/delete/', views.StudentDeleteView.as_view(), name='delete'),

    # Parents
    path('parents/', views.ParentListView.as_view(), name='parent_list'),
    path('parents/create/', views.parent_create, name='parent_create'),
    path('parents/<int:pk>/update/', views.parent_update, name='parent_update'),
    path('parents/<int:pk>/delete/', views.ParentDeleteView.as_view(), name='parent_delete'),
]
