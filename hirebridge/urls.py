from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
     path('dashboard/', views.dashboard, name='dashboard'),
     path('logout/', views.user_logout, name='logout'),
     path('profile/', views.profile, name='profile'),
     path('create-resume/', views.create_resume, name='create_resume'),
     path('resume/<int:resume_id>/education/', views.add_education, name='add_education'),
     path(
    'resume/<int:resume_id>/education/<int:education_id>/edit/',
    views.edit_education,
    name='edit_education'
),
path(
    'resume/<int:resume_id>/skill/<int:skill_id>/edit/',
    views.edit_skill,
    name='edit_skill'
),
path(
    'resume/<int:resume_id>/project/<int:project_id>/edit/',
    views.edit_project,
    name='edit_project'
),
path(
    'resume/<int:resume_id>/certification/<int:certification_id>/edit/',
    views.edit_certification,
    name='edit_certification'
),
     path('resume/<int:resume_id>/skill/', views.add_skill, name='add_skill'),
     path(
    'resume/<int:resume_id>/work-experience/',
    views.add_work_experience,
    name='add_work_experience'
),

path(
    'resume/<int:resume_id>/work-experience/<int:work_id>/edit/',
    views.edit_work_experience,
    name='edit_work_experience'
),


path(
    'resume/<int:resume_id>/project/',
    views.add_project,
    name='add_project'
),
path(
    'resume/<int:resume_id>/certification/',
    views.add_certification,
    name='add_certification'
),
path(
    'resume/<int:resume_id>/upload-cv/',
    views.upload_cv,
    name='upload_cv'
),
path(
    'resume/<int:resume_id>/analyze/',
    views.analyze_cv,
    name='analyze_cv'
),
]

