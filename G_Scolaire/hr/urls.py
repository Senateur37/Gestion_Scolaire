from django.urls import path
from . import views

app_name = 'hr'

urlpatterns = [
    # Staff
    path('staff/', views.StaffListView.as_view(), name='staff_list'),
    path('staff/create/', views.StaffCreateView.as_view(), name='staff_create'),
    path('staff/<int:pk>/update/', views.StaffUpdateView.as_view(), name='staff_update'),
    path('staff/<int:pk>/delete/', views.StaffDeleteView.as_view(), name='staff_delete'),
    
    # Leave
    path('leave/', views.LeaveListView.as_view(), name='leave_list'),
    path('leave/request/', views.LeaveCreateView.as_view(), name='leave_create'),
    path('leave/<int:pk>/approve/', views.approve_leave, name='leave_approve'),
    path('leave/<int:pk>/reject/', views.reject_leave, name='leave_reject'),
    
    # Payroll
    path('payroll/', views.PayrollListView.as_view(), name='payroll_list'),
    path('payroll/generate/', views.generate_payroll, name='payroll_generate'),
    path('payroll/<int:pk>/pay/', views.mark_paid, name='payroll_pay'),
]
