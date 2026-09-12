import re

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
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
    CVUploadForm
)

from .models import (
    Resume,
    CVScore,
    ScoreDetail,
    Suggestion,
    ScoringCriteria,
)


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

    user_profile = request.user.profile

    resumes = Resume.objects.filter(
        user=user_profile
    )

    return render(
        request,
        'dashboard.html',
        {'resumes': resumes}
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


def upload_cv(request, resume_id):
    if not request.user.is_authenticated:
        return redirect('login')

    user_profile = request.user.profile

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=user_profile
    )

    if request.method == 'POST':
        form = CVUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            uploaded_file = request.FILES.get('file_path')

            cv_upload = form.save(commit=False)
            cv_upload.resume = resume

            if uploaded_file:
                cv_upload.file_name = uploaded_file.name

            cv_upload.save()

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
            'resume': resume
        }
    )


def analyze_cv(request, resume_id):
    if not request.user.is_authenticated:
        return redirect('login')

    user_profile = request.user.profile

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=user_profile
    )

    keywords = {
        'Education': [
            'bachelor',
            'master',
            'bim',
            'bca',
            'computer',
            'information technology',
            'management'
        ],
        'Skills': [
            'python',
            'django',
            'java',
            'javascript',
            'html',
            'css',
            'mysql',
            'sql',
            'git',
            'github'
        ],
        'Work Experience': [
            'intern',
            'internship',
            'developer',
            'software',
            'web',
            'project',
            'experience'
        ],
        'Projects': [
            'python',
            'django',
            'website',
            'web',
            'database',
            'mysql',
            'javascript',
            'system',
            'application'
        ],
        'Certifications': [
            'certificate',
            'certification',
            'python',
            'django',
            'database',
            'web development'
        ]
    }

    section_text = {
        'Education': '',
        'Skills': '',
        'Work Experience': '',
        'Projects': '',
        'Certifications': ''
    }

    for education in resume.education.all():
        section_text['Education'] += (
            ' ' +
            (education.degree or '') +
            ' ' +
            (education.institution or '')
        )

    for skill in resume.skills.all():
        section_text['Skills'] += (
            ' ' +
            (skill.skill_name or '') +
            ' ' +
            (skill.skill_level or '')
        )

    for work in resume.work_experience.all():
        section_text['Work Experience'] += (
            ' ' +
            (work.job_title or '') +
            ' ' +
            (work.company_name or '') +
            ' ' +
            (work.description or '')
        )

    for project in resume.projects.all():
        section_text['Projects'] += (
            ' ' +
            (project.project_name or '') +
            ' ' +
            (project.description or '') +
            ' ' +
            (project.technologies_used or '')
        )

    for certification in resume.certifications.all():
        section_text['Certifications'] += (
            ' ' +
            (certification.certification_name or '') +
            ' ' +
            (certification.issuing_organization or '') +
            ' ' +
            (certification.credential_id or '')
        )

    for section in section_text:
        section_text[section] = section_text[section].lower()

    scoring_criteria = {}

    for criteria_name in keywords:
        scoring_criteria[criteria_name] = (
            ScoringCriteria.objects.get(
                criteria_name=criteria_name
            )
        )

    criteria_scores = {}

    for criteria_name, keyword_list in keywords.items():

        maximum_score = scoring_criteria[
            criteria_name
        ].maximum_score

        matched_keywords = []

        for keyword in keyword_list:

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

        if matched_keywords:
            points_per_keyword = (
                maximum_score / len(keyword_list)
            )

            obtained_score = round(
                len(matched_keywords) * points_per_keyword
            )

        else:
            obtained_score = 0

        criteria_scores[criteria_name] = min(
            obtained_score,
            maximum_score
        )

    total_score = sum(
        criteria_scores.values()
    )

    previous_score = (
        resume.scores
        .order_by('-scored_date')
        .first()
    )

    if previous_score:
        previous_score.details.all().delete()
        previous_score.suggestions.all().delete()
        previous_score.delete()

    cv_score = CVScore.objects.create(
        resume=resume,
        score=total_score
    )

    for criteria_name, obtained_score in criteria_scores.items():
        ScoreDetail.objects.create(
            cv_score=cv_score,
            criteria=scoring_criteria[criteria_name],
            obtained_score=obtained_score
        )

    suggestions = []

    if criteria_scores['Education'] < scoring_criteria[
        'Education'
    ].maximum_score:
        suggestions.append(
            'Add relevant education details and qualifications to your CV.'
        )

    if criteria_scores['Skills'] < scoring_criteria[
        'Skills'
    ].maximum_score:
        suggestions.append(
            'Add more relevant technical and professional skills such as Python, Django, SQL, JavaScript, Git or HTML/CSS.'
        )

    if criteria_scores['Work Experience'] < scoring_criteria[
        'Work Experience'
    ].maximum_score:
        suggestions.append(
            'Add relevant work or internship experience with clear responsibilities.'
        )

    if criteria_scores['Projects'] < scoring_criteria[
        'Projects'
    ].maximum_score:
        suggestions.append(
            'Add relevant projects and mention the technologies used.'
        )

    if criteria_scores['Certifications'] < scoring_criteria[
        'Certifications'
    ].maximum_score:
        suggestions.append(
            'Add relevant certifications and credential information.'
        )

    for suggestion_text in suggestions:
        Suggestion.objects.create(
            cv_score=cv_score,
            suggestion_text=suggestion_text
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

