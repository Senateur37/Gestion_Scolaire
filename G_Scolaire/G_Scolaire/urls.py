from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('system/', include('accounts.urls')),
    path('', include('dashboards.urls')),
    path('students/', include('students.urls')),
    path('teachers/', include('teachers.urls')),
    path('academics/', include('academics.urls')),
    path('payments/', include('payments.urls')),
    path('library/', include('library.urls')),
    path('transport/', include('transport.urls')),
    path('hostel/', include('hostel.urls')),
    path('exams/', include('exams.urls')),
    path('reports/', include('reports.urls')),
    path('attendance/', include('attendance.urls')),
    path('hr/', include('hr.urls')),
    path('communication/', include('communication.urls')),
    path('inventory/', include('inventory.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
