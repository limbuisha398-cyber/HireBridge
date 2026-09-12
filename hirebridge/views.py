import re

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import (
    RegistrationForm,
    ProfileForm,
    ResumeForm,
    EducationForm,
    SkillForm,
    WorkExperienceForm,
    ProjectForm,
    CertificationForm,
    CVUploadForm,
)

from .models import (
    UserProfile,
    Resume,
    Education,
    Skill,
    Project,
    CVScore,
    Suggestion,
    ScoreDetail,
    ScoringCriteria
)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Registration successful. Please login.'
            )
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(
        request,
        'register.html',
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

    return render(request, 'registration/login.html')


@login_required
def dashboard(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    resumes = Resume.objects.filter(user=profile).prefetch_related('education')

    return render(
        request,
        'dashboard.html',
        {'resumes': resumes}
    )

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    if request.method == 'POST':
        form = ProfileForm(
            request.POST,
            instance=profile,
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
            instance=profile,
            user=request.user
        )

    return render(
        request,
        'profile.html',
        {
            'form': form,
            'profile': profile,
        }
    )


@login_required
def create_resume(request):
    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    if request.method == 'POST':
        form = ResumeForm(request.POST)

        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = profile
            resume.save()

            return redirect(
                'add_education',
                resume_id=resume.id
            )
    else:
        form = ResumeForm()

    return render(
        request,
        'create_resume.html',
        {'form': form}
    )


@login_required
def add_education(request, resume_id):
    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user__user=request.user
    )

    if request.method == 'POST':
        form = EducationForm(request.POST)

        if form.is_valid():
            education = form.save(commit=False)
            education.resume = resume
            education.save()

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
            'resume': resume,
        }
    )


@login_required
def edit_education(request, resume_id, education_id):
    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user__user=request.user
    )

    education = get_object_or_404(
        Education,
        id=education_id,
        resume=resume
    )

    if request.method == 'POST':
        form = EducationForm(
            request.POST,
            instance=education
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Education updated successfully.'
            )

            return redirect('dashboard')
    else:
        form = EducationForm(
            instance=education
        )

    return render(
        request,
        'edit_education.html',
        {
            'form': form,
            'resume': resume,
            'education': education,
        }
    )
@login_required
def edit_skill(request, resume_id, skill_id):
    profile = get_object_or_404(UserProfile, user=request.user)
    resume = get_object_or_404(Resume, id=resume_id, user=profile)
    skill = get_object_or_404(Skill, id=skill_id, resume=resume)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)

        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated successfully.')
            return redirect('dashboard')
    else:
        form = SkillForm(instance=skill)

    return render(
        request,
        'edit_skill.html',
        {
            'form': form,
            'resume': resume,
            'skill': skill
        }
    )
@login_required
def edit_project(request, resume_id, project_id):
    profile = get_object_or_404(UserProfile, user=request.user)
    resume = get_object_or_404(Resume, id=resume_id, user=profile)
    project = get_object_or_404(Project, id=project_id, resume=resume)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully.')
            return redirect('dashboard')
    else:
        form = ProjectForm(instance=project)

    return render(
        request,
        'edit_project.html',
        {
            'form': form,
            'resume': resume,
            'project': project
        }
    )


@login_required
def add_skill(request, resume_id):
    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user__user=request.user
    )

    if request.method == 'POST':
        form = SkillForm(request.POST)

        if form.is_valid():
            skill = form.save(commit=False)
            skill.resume = resume
            skill.save()

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
            'resume': resume,
        }
    )


@login_required
def add_work_experience(request, resume_id):
    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user__user=request.user
    )

    if request.method == 'POST':
        form = WorkExperienceForm(request.POST)

        if form.is_valid():
            work = form.save(commit=False)
            work.resume = resume
            work.save()

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
            'resume': resume,
        }
    )


@login_required
def add_project(request, resume_id):
    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user__user=request.user
    )

    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.resume = resume
            project.save()

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
            'resume': resume,
        }
    )


@login_required
def add_certification(request, resume_id):
    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user__user=request.user
    )

    if request.method == 'POST':
        form = CertificationForm(request.POST)

        if form.is_valid():
            certification = form.save(commit=False)
            certification.resume = resume
            certification.save()

            return redirect(
                'dashboard'
            )
    else:
        form = CertificationForm()

    return render(
        request,
        'add_certification.html',
        {
            'form': form,
            'resume': resume,
        }
    )


@login_required
def upload_cv(request, resume_id):
    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user__user=request.user
    )

    if request.method == 'POST':
        form = CVUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            upload = form.save(commit=False)
            upload.resume = resume
            upload.file_name = upload.file_path.name
            upload.save()

            messages.success(
                request,
                'CV uploaded successfully.'
            )

            return redirect(
                'upload_cv',
                resume_id=resume.id
            )
    else:
        form = CVUploadForm()

    return render(
        request,
        'upload_cv.html',
        {
            'form': form,
            'resume': resume,
        }
    )


@login_required
def analyze_cv(request, resume_id):
    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user__user=request.user
    )

    criteria_list = ScoringCriteria.objects.all()

    section_text = {
        'Education': ' '.join(
            f'{education.degree} '
            f'{education.institution}'
            for education in resume.education.all()
        ).lower(),

        'Skills': ' '.join(
            f'{skill.skill_name} '
            f'{skill.skill_level}'
            for skill in resume.skills.all()
        ).lower(),

        'Work Experience': ' '.join(
            f'{work.job_title} '
            f'{work.company_name} '
            f'{work.description}'
            for work in resume.work_experience.all()
        ).lower(),

        'Projects': ' '.join(
            f'{project.project_name} '
            f'{project.description} '
            f'{project.technologies_used}'
            for project in resume.projects.all()
        ).lower(),

        'Certifications': ' '.join(
            f'{certification.certification_name} '
            f'{certification.issuing_organization} '
            f'{certification.credential_id}'
            for certification in resume.certifications.all()
        ).lower(),
    }

    keywords = {
        'Education': [
            'bachelor',
            'master',
            'degree',
            'bim',
            'computer',
            'information technology',
            'education',
            'university',
        ],

        'Skills': [
            'python',
            'django',
            'sql',
            'javascript',
            'git',
            'html',
            'css',
            'mysql',
            'database',
        ],

        'Work Experience': [
            'intern',
            'internship',
            'developer',
            'experience',
            'responsibility',
            'project',
            'software',
            'web',
        ],

        'Projects': [
            'project',
            'django',
            'python',
            'mysql',
            'html',
            'css',
            'javascript',
            'github',
        ],

        'Certifications': [
            'certificate',
            'certification',
            'credential',
            'training',
            'course',
            'workshop',
        ],
    }

    CVScore.objects.filter(
        resume=resume
    ).delete()

    total_score = 0
    score_details = []

    for criteria in criteria_list:
        criteria_name = criteria.criteria_name
        matched_keywords = []

        for keyword in keywords.get(
            criteria_name,
            []
        ):
            keyword_pattern = (
                r'\b' +
                re.escape(keyword.lower()) +
                r'\b'
            )

            if re.search(
                keyword_pattern,
                section_text[criteria_name]
            ):
                matched_keywords.append(keyword)

        keyword_count = len(matched_keywords)
        max_score = criteria.maximum_score

        if keyword_count > 0:
            obtained_score = min(
                max_score,
                keyword_count * 3
            )
        else:
            obtained_score = 0

        score_details.append(
            (
                criteria,
                obtained_score
            )
        )

        total_score += obtained_score

    cv_score = CVScore.objects.create(
        resume=resume,
        score=total_score
    )

    for criteria, obtained_score in score_details:
        ScoreDetail.objects.create(
            cv_score=cv_score,
            criteria=criteria,
            obtained_score=obtained_score
        )

        if obtained_score == 0:
            Suggestion.objects.create(
                cv_score=cv_score,
                suggestion_text=(
                    f'Add relevant {criteria.criteria_name.lower()} '
                    'details to your CV.'
                )
            )

        elif obtained_score < criteria.maximum_score:
            Suggestion.objects.create(
                cv_score=cv_score,
                suggestion_text=(
                    f'Add more relevant {criteria.criteria_name.lower()} '
                    'details and keywords to improve your score.'
                )
            )

    return render(
        request,
        'cv_analysis.html',
        {
            'resume': resume,
            'cv_score': cv_score,
            'score_details': cv_score.details.all(),
            'suggestions': cv_score.suggestions.all(),
        }
    )