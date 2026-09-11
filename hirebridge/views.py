from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import RegistrationForm, ProfileForm, ResumeForm, EducationForm, SkillForm, WorkExperienceForm, ProjectForm, CertificationForm
from .models import Resume
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
def create_resume(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_profile = request.user.profile

    if request.method == 'POST':
        form = ResumeForm(request.POST)

        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = user_profile
            resume.save()

            messages.success(
                request,
                'CV created successfully.'
            )

            return redirect('add_education', resume_id=resume.id)
    else:
        form = ResumeForm()

    return render(
        request,
        'create_resume.html',
        {'form': form}
    )


def add_education(request, resume_id):
    if not request.user.is_authenticated:
        return redirect('login')

    user_profile = request.user.profile

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=user_profile
    )

    if request.method == 'POST':
        form = EducationForm(request.POST)

        if form.is_valid():
            education = form.save(commit=False)
            education.resume = resume
            education.save()

            messages.success(
                request,
                'Education added successfully.'
            )

            return redirect(
                'add_skill',
                resume_id=resume.id
         )
            

    else:
        form = EducationForm()

    return render(
        request,
        'add_education.html',
        {
            'form': form,
            'resume': resume
        }
    )
def add_work_experience(request, resume_id):
    if not request.user.is_authenticated:
        return redirect('login')

    user_profile = request.user.profile

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=user_profile
    )

    if request.method == 'POST':
        form = WorkExperienceForm(request.POST)

        if form.is_valid():
            work_experience = form.save(commit=False)
            work_experience.resume = resume
            work_experience.save()

            messages.success(
                request,
                'Work experience added successfully.'
            )

            return redirect(
                'add_project',
                resume_id=resume.id
            )

    else:
        form = WorkExperienceForm()

    return render(
        request,
        'add_work_experience.html',
        {
            'form': form,
            'resume': resume
        }
    )
def add_skill(request, resume_id):
    if not request.user.is_authenticated:
        return redirect('login')

    user_profile = request.user.profile

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=user_profile
    )

    if request.method == 'POST':
        form = SkillForm(request.POST)

        if form.is_valid():
            skill = form.save(commit=False)
            skill.resume = resume
            skill.save()

            messages.success(
                request,
                'Skill added successfully.'
            )

            return redirect(
                'add_work_experience',
                resume_id=resume.id
            )

    else:
        form = SkillForm()

    return render(
        request,
        'add_skill.html',
        {
            'form': form,
            'resume': resume
        }
    )
def add_project(request, resume_id):
    if not request.user.is_authenticated:
        return redirect('login')

    user_profile = request.user.profile

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=user_profile
    )

    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.resume = resume
            project.save()

            messages.success(
                request,
                'Project added successfully.'
            )

            return redirect(
                'add_certification',
                resume_id=resume.id
            )

    else:
        form = ProjectForm()

    return render(
        request,
        'add_project.html',
        {
            'form': form,
            'resume': resume
        }
    )
def add_certification(request, resume_id):
    if not request.user.is_authenticated:
        return redirect('login')

    user_profile = request.user.profile

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=user_profile
    )

    if request.method == 'POST':
        form = CertificationForm(request.POST)

        if form.is_valid():
            certification = form.save(commit=False)
            certification.resume = resume
            certification.save()

            messages.success(
                request,
                'Certification added successfully.'
            )

            return redirect(
                'add_certification',
                resume_id=resume.id
            )

    else:
        form = CertificationForm()

    return render(
        request,
        'add_certification.html',
        {
            'form': form,
            'resume': resume
        }
    )
