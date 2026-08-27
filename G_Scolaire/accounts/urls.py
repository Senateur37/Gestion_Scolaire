from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
]
