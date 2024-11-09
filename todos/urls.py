from django.urls import path
from . import views

urlpatterns = [
   
    path('todo/<int:id>/toggle/', views.todo_toggle_status, name='todo_toggle_status'),
    path('todo/<int:id>/delete/', views.todo_delete, name='todo_delete'),
]