from django.shortcuts import render

from django.shortcuts import get_object_or_404, redirect
from .models import Todo

def todo_toggle_status(request, id):
    todo = get_object_or_404(Todo, id=id)
    todo.status = not todo.status 
    todo.save()
    return redirect('project_detail', id=todo.project.id)



def todo_delete(request, id):
    todo = get_object_or_404(Todo, id=id)  # Get the Todo object
    project_id = todo.project.id  # Get the project associated with the todo
    todo.delete()  # Delete  todo item
    return redirect('project_detail', id=project_id)  
