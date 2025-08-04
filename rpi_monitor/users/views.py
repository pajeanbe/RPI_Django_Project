from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserEditForm
from .models import CustomUser

def is_admin(user):
    return user.is_superuser or user.is_monitoring_admin

@user_passes_test(is_admin)
def user_management(request):
    users = CustomUser.objects.all()
    return render(request, 'users/management.html', {'users': users})

@user_passes_test(is_admin)
def create_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} created successfully.')
            return redirect('users:management')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/create.html', {'form': form})

@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.username} updated successfully.')
            return redirect('users:management')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'users/edit.html', {'form': form, 'user': user})

@login_required
def profile(request):
    return render(request, 'users/profile.html')