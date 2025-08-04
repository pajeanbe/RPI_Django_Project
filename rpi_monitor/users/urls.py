from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('management/', views.user_management, name='management'),
    path('create/', views.create_user, name='create'),
    path('edit/<int:user_id>/', views.edit_user, name='edit'),
    path('profile/', views.profile, name='profile'),
]