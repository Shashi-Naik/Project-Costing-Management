from django.urls import path
from . import views

urlpatterns = [
    # Serve HTML Pages
    path('reports/form/', views.report_form, name='report_form'),
    path('reports/view/', views.report_list, name='report_list'),
    path('reports/edit/<int:report_id>/', views.edit_report, name='edit_report'),

    # REST API Endpoints
    path('reports/', views.get_reports, name='get_reports'),
    path('reports/<int:report_id>/', views.get_report_by_id, name='get_report_by_id'),
    path('reports/create/', views.create_report, name='create_report'),
    path('reports/<int:report_id>/update/', views.update_report, name='update_report'),
    path('reports/<int:report_id>/delete/', views.delete_report, name='delete_report'),
]
