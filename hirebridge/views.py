from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, ProfileForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Registration successful. You can now log in.'
            )
            return redirect('login')

    else:
        form = RegistrationForm()

    return render(
        request,
        'registration/register.html',
        {'form': form}
    )
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(
        request,
        'registration/login.html'
    )
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(
        request,
        'dashboard.html'
    )
def user_logout(request):
    logout(request)
    return redirect('login')
def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(
            request.POST,
            instance=user_profile,
            user=request.user
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Profile updated successfully.'
            )
            return redirect('profile')

    else:
        form = ProfileForm(
            instance=user_profile,
            user=request.user
        )

    return render(
        request,
        'profile.html',
        {'form': form}
    )

