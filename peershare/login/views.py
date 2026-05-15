from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, RegisterForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                messages.success(
                    request,
                    f'👋 Welcome back, {user.username}!'
                )
                return redirect('/dashboard/')
            else:
                messages.error(
                    request,
                    '❌ Wrong username or password.'
                )
    else:
        form = LoginForm()

    return render(request, 'login/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.university_email = form.cleaned_data['university_email']
            user.save()
            login(request, user)
            messages.success(
                request,
                '🎉 Welcome to PeerShare!'
            )
            return redirect('/dashboard/')
        else:
            messages.error(request, '⚠️ Please fix the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'login/register.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.info(request, '👋 Logged out successfully.')
    return redirect('/login/')