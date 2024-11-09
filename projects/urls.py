from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('project/<int:id>/', views.project_detail, name='project_detail'),
    path('project/<int:id>/export/', views.export_project_summary, name='export_project_summary'),
]

