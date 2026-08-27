from django.urls import path
from . import views

app_name = 'hostel'

urlpatterns = [
    path('hostels/', views.HostelListView.as_view(), name='hostel_list'),
    path('hostels/create/', views.HostelCreateView.as_view(), name='hostel_create'),
    path('hostels/<int:pk>/update/', views.HostelUpdateView.as_view(), name='hostel_update'),
    path('hostels/<int:pk>/delete/', views.HostelDeleteView.as_view(), name='hostel_delete'),
    
    path('rooms/', views.RoomListView.as_view(), name='room_list'),
    path('rooms/create/', views.RoomCreateView.as_view(), name='room_create'),
    path('rooms/<int:pk>/update/', views.RoomUpdateView.as_view(), name='room_update'),
    path('rooms/<int:pk>/delete/', views.RoomDeleteView.as_view(), name='room_delete'),
]
