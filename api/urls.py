from django.urls import path

from . import views

urlpatterns = [
    path('register-user/', views.register_user),
    path('tasks/', views.get_tasks),
    path('specializations/', views.get_specializations),
    path('download-attendance-report/', views.download_attendance_report, name="download_attendance_report"),
]
