from django.urls import path
from . import views

app_name = 'transport'

urlpatterns = [
    path('routes/', views.RouteListView.as_view(), name='route_list'),
    path('routes/create/', views.RouteCreateView.as_view(), name='route_create'),
    path('routes/<int:pk>/update/', views.RouteUpdateView.as_view(), name='route_update'),
    path('routes/<int:pk>/delete/', views.RouteDeleteView.as_view(), name='route_delete'),
    
    path('vehicles/', views.VehicleListView.as_view(), name='vehicle_list'),
    path('vehicles/create/', views.VehicleCreateView.as_view(), name='vehicle_create'),
    path('vehicles/<int:pk>/update/', views.VehicleUpdateView.as_view(), name='vehicle_update'),
    path('vehicles/<int:pk>/delete/', views.VehicleDeleteView.as_view(), name='vehicle_delete'),
]
