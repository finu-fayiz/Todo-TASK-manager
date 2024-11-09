"""
URL configuration for todo_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""



from django.contrib import admin
from django.urls import path, include
from projects import views as project_views
from accounts.views import user_register  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # For login & logout
    path('accounts/register/', user_register, name='user_register'),  # Register URL
    path('projects/', include('projects.urls')),  # Projects URLS
    path('todos/', include('todos.urls')),  # Todos URLS
    path('', project_views.home, name='home'),  # Home page URL
]
