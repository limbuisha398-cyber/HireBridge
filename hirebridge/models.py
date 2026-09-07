from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ---------- 1 & 2: USER, USER_PHONE ----------
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class UserPhone(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='phones')
    phone_number = models.CharField(max_length=20)


# ---------- 3 & 4: ADMIN, ADMIN_PHONE ----------
class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class AdminPhone(models.Model):
    admin_profile = models.ForeignKey(AdminProfile, on_delete=models.CASCADE, related_name='phones')
    phone_number = models.CharField(max_length=20)


# ---------- 5: RESUME ----------
class Resume(models.Model):
    STATUS_CHOICES = (('draft', 'Draft'), ('completed', 'Completed'))
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='resumes')
    admin = models.ForeignKey(AdminProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_resumes')
    title = models.CharField(max_length=150)
    date_created = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return f"{self.title} - {self.user.user.username}"


# ---------- 6: EDUCATION ----------
class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=150)
    institution = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)


# ---------- 7: SKILL ----------
class Skill(models.Model):
    LEVEL_CHOICES = (('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced'))
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(max_length=100)
    skill_level = models.CharField(max_length=15, choices=LEVEL_CHOICES, default='beginner')


# ---------- 8: WORK_EXPERIENCE ----------
class WorkExperience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='work_experience')
    job_title = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)


# ---------- 9: PROJECT ----------
class Project(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='projects')
    project_name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    technologies_used = models.CharField(max_length=255, blank=True)
    project_link = models.URLField(blank=True)


# ---------- 10: CERTIFICATION ----------
class Certification(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='certifications')
    certification_name = models.CharField(max_length=150)
    issuing_organization = models.CharField(max_length=150, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)




# ---------- 11: CV_UPLOAD ----------
class CVUpload(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='uploads')
    file_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='uploaded_cvs/')
    upload_date = models.DateTimeField(auto_now_add=True)


# ---------- 14: SCORING_CRITERIA ----------
class ScoringCriteria(models.Model):
    criteria_name = models.CharField(max_length=100, unique=True)
    maximum_score = models.IntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.criteria_name} (max {self.maximum_score})"


# ---------- 12: CV_SCORE ----------
class CVScore(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='scores')
    score = models.IntegerField(default=0)
    scored_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resume.title}: {self.score}"


# ---------- 13: SUGGESTION ----------
class Suggestion(models.Model):
    cv_score = models.ForeignKey(CVScore, on_delete=models.CASCADE, related_name='suggestions')
    suggestion_text = models.CharField(max_length=255)
    suggestion_date = models.DateTimeField(auto_now_add=True)


# ---------- 15: SCORE_DETAIL ----------
class ScoreDetail(models.Model):
    cv_score = models.ForeignKey(CVScore, on_delete=models.CASCADE, related_name='details')
    criteria = models.ForeignKey(ScoringCriteria, on_delete=models.CASCADE)
    obtained_score = models.IntegerField()

# ---------- 16: APPLICATION ----------
class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    )

    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    admin = models.ForeignKey(
        AdminProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applications'
    )
    position = models.CharField(max_length=150)
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return f"{self.user.user.username} - {self.position}"
