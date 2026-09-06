from django.contrib import admin
from .models import (
    UserProfile, UserPhone, AdminProfile, AdminPhone, Resume,
    Education, Skill, WorkExperience, Project, Certification,
    CVUpload, CVScore, Suggestion, ScoringCriteria, ScoreDetail
)

admin.site.register([
    UserProfile, UserPhone, AdminProfile, AdminPhone, Resume,
    Education, Skill, WorkExperience, Project, Certification,
    CVUpload, CVScore, Suggestion, ScoringCriteria, ScoreDetail
])