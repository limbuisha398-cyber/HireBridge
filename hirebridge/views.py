from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import re
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
    WorkExperience,
    Project,
    Certification,
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
    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    resumes = Resume.objects.filter(user=profile)

    return render(
        request,
        'dashboard.html',
        {
            'profile': profile,
            'resumes': resumes,
        }
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
def edit_certification(request, resume_id, certification_id):
    profile = get_object_or_404(UserProfile, user=request.user)
    resume = get_object_or_404(Resume, id=resume_id, user=profile)
    certification = get_object_or_404(
        Certification,
        id=certification_id,
        resume=resume
    )

    if request.method == 'POST':
        form = CertificationForm(
            request.POST,
            instance=certification
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Certification updated successfully.'
            )
            return redirect('dashboard')
    else:
        form = CertificationForm(instance=certification)

    return render(
        request,
        'edit_certification.html',
        {
            'form': form,
            'resume': resume,
            'certification': certification
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
def edit_work_experience(request, resume_id, work_id):
    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=profile
    )

    work = get_object_or_404(
        WorkExperience,
        id=work_id,
        resume=resume
    )

    if request.method == 'POST':
        form = WorkExperienceForm(
            request.POST,
            instance=work
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Work experience updated successfully.'
            )
            return redirect('dashboard')
    else:
        form = WorkExperienceForm(instance=work)

    return render(
        request,
        'edit_work_experience.html',
        {
            'form': form,
            'resume': resume,
            'work': work
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
@login_required
def download_cv(request, resume_id):
    profile, created = UserProfile.objects.get_or_create(
    user=request.user
)
    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=profile
    )

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CVTitle',
        parent=styles['Title'],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=10
    )

    heading_style = ParagraphStyle(
        'CVHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=12,
        spaceAfter=6
    )

    normal_style = ParagraphStyle(
        'CVNormal',
        parent=styles['BodyText'],
        fontSize=10,
        leading=14,
        spaceAfter=4
    )

    story = []

    full_name = request.user.get_full_name() or request.user.username

    story.append(
        Paragraph(full_name, title_style)
    )

    story.append(
        Paragraph(resume.title, styles['Heading1'])
    )

    if profile.address:
        story.append(
            Paragraph(
                f"Address: {profile.address}",
                normal_style
            )
        )

    phone_numbers = profile.phones.all()

    for phone in phone_numbers:
        story.append(
            Paragraph(
                f"Phone: {phone.phone_number}",
                normal_style
            )
        )

    story.append(Spacer(1, 10))

    education_list = resume.education.all()

    if education_list.exists():
        story.append(
            Paragraph("Education", heading_style)
        )

        for education in education_list:
            end_date = (
                education.end_date.strftime("%Y-%m-%d")
                if education.end_date
                else "Present"
            )

            story.append(
                Paragraph(
                    f"<b>{education.degree}</b> - "
                    f"{education.institution}<br/>"
                    f"{education.start_date.strftime('%Y-%m-%d')} "
                    f"to {end_date}",
                    normal_style
                )
            )

    skills = resume.skills.all()

    if skills.exists():
        story.append(
            Paragraph("Skills", heading_style)
        )

        for skill in skills:
            story.append(
                Paragraph(
                    f"{skill.skill_name} "
                    f"({skill.get_skill_level_display()})",
                    normal_style
                )
            )

    work_experiences = resume.work_experience.all()

    if work_experiences.exists():
        story.append(
            Paragraph("Work Experience", heading_style)
        )

        for work in work_experiences:
            end_date = (
                work.end_date.strftime("%Y-%m-%d")
                if work.end_date
                else "Present"
            )

            story.append(
                Paragraph(
                    f"<b>{work.job_title}</b> - "
                    f"{work.company_name}<br/>"
                    f"{work.start_date.strftime('%Y-%m-%d')} "
                    f"to {end_date}",
                    normal_style
                )
            )

            if work.description:
                story.append(
                    Paragraph(
                        work.description,
                        normal_style
                    )
                )

    projects = resume.projects.all()

    if projects.exists():
        story.append(
            Paragraph("Projects", heading_style)
        )

        for project in projects:
            story.append(
                Paragraph(
                    f"<b>{project.project_name}</b>",
                    normal_style
                )
            )

            if project.description:
                story.append(
                    Paragraph(
                        project.description,
                        normal_style
                    )
                )

            if project.technologies_used:
                story.append(
                    Paragraph(
                        f"Technologies: {project.technologies_used}",
                        normal_style
                    )
                )

            if project.project_link:
                story.append(
                    Paragraph(
                        f"Project Link: {project.project_link}",
                        normal_style
                    )
                )

    certifications = resume.certifications.all()

    if certifications.exists():
        story.append(
            Paragraph("Certifications", heading_style)
        )

        for certification in certifications:
            text = (
                f"<b>{certification.certification_name}</b>"
            )

            if certification.issuing_organization:
                text += (
                    f" - {certification.issuing_organization}"
                )

            if certification.issue_date:
                text += (
                    f"<br/>Issue Date: "
                    f"{certification.issue_date.strftime('%Y-%m-%d')}"
                )

            if certification.expiry_date:
                text += (
                    f"<br/>Expiry Date: "
                    f"{certification.expiry_date.strftime('%Y-%m-%d')}"
                )

            if certification.credential_id:
                text += (
                    f"<br/>Credential ID: "
                    f"{certification.credential_id}"
                )

            story.append(
                Paragraph(
                    text,
                    normal_style
                )
            )

    document.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(
        pdf,
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="{resume.title}.pdf"'
    )

    return response