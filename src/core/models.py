from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from core.managers import UserManager


class User(AbstractUser):

    class UserType(models.TextChoices):
        JOB_RECRUITER = 'recruiter', 'Job Recruiter'
        JOB_SEEKER = 'seeker', 'Job Seeker'

    objects = UserManager()
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    first_name = models.CharField(_('First Name'), max_length=50)
    last_name = models.CharField(_('Last Name'), max_length=50)
    email = models.EmailField(_('Email Address'), unique=True)
    user_type = models.CharField(_('Join As'), max_length=10, choices=UserType.choices)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user'


class Job(models.Model):

    title = models.CharField(max_length=60)
    description = models.TextField(validators=[MinLengthValidator(30)])
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    applicants = models.ManyToManyField(User)

    class Meta:
        db_table = 'job'
        ordering = ['id']
