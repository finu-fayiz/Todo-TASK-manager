from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from .forms import ProjectForm
from todos.forms import TodoForm
from django.contrib.auth.decorators import login_required
import requests
import os 
from django.conf import settings


def home(request):
    projects = Project.objects.all()
    return render(request, 'projects/home.html', {'projects': projects})


@login_required
def project_list(request):
   
    projects = Project.objects.filter(user=request.user) #all project for present user

    
    form = ProjectForm(request.POST or None)
    if request.method == 'POST':                 #form submission for creating a new project
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user         
            project.save()
            return redirect('project_list')      

    
    return render(request, 'projects/project_list.html', {
        'projects': projects,                    
        'form': form,  
    })

@login_required
def project_detail(request, id):
    project = get_object_or_404(Project, id=id, user=request.user)
    todos = project.todos.all()

    if request.method == 'POST':
        if 'todo' in request.POST:
            todo_form = TodoForm(request.POST)
            if todo_form.is_valid():
                todo = todo_form.save(commit=False)
                todo.project = project
                todo.save()
                return redirect('project_detail', id=project.id)
        else:
            title_form = ProjectForm(request.POST, instance=project)
            if title_form.is_valid():
                title_form.save()
                return redirect('project_detail', id=project.id)

    else:
        todo_form = TodoForm()
        title_form = ProjectForm(instance=project)

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'todos': todos,
        'todo_form': todo_form,
        'title_form': title_form
    })

def export_project_summary(request, id):
    project = get_object_or_404(Project, id=id, user=request.user)
    todos = project.todos.all()
    github_token = settings.GITHUB_TOKEN

    # Markdown  for Gist
    completed_todos = todos.filter(status=True).count()
    total_todos = todos.count()
    markdown = f"# {project.title}\n\n"
    markdown += f"**Summary:** {completed_todos} / {total_todos} completed\n\n"

    # Pending Todos
    markdown += "## Pending Todos\n"
    for todo in todos.filter(status=False):
        markdown += f"- [ ] {todo.description} (Created: {todo.created_date})\n"
    
    # Completed Todos
    markdown += "## Completed Todos\n"
    for todo in todos.filter(status=True):
        markdown += f"- [x] {todo.description} (Created: {todo.created_date}, Updated: {todo.updated_date})\n"

    # Save the markdown file in media
    file_name = f"{project.title}_summary.md"
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    # Write the markdown content to a file
    with open(file_path, 'w') as file:
        file.write(markdown)

    # Gist data for GitHub API
    gist_data = {
        "files": {f"{project.title}.md": {"content": markdown}},
        "public": False
    }

    # Request to GitHub API
    headers = {"Authorization": f"token {github_token}"}
    response = requests.post("https://api.github.com/gists", json=gist_data, headers=headers)

    # Success or failure
    if response.status_code == 201:
        gist_url = response.json().get('html_url')

        # After successfully creating the Gist, redirect to the Gist URL
        return redirect(gist_url)
    
    # If  fails, return an error message
    return render(request, 'projects/project_list.html', {
        'projects': Project.objects.filter(user=request.user),
        'error': "Failed to export summary as Gist. Please try again."
    })