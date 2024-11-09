from django.urls import path
from .views import user_register  # register view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/register/', user_register, name='user_register'),
     path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
