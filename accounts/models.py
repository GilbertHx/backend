import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    PROFILE_TYPE_CHOICES = (
        ('R', 'REG'),
        ('S', 'STUDENT'),
        ('U', 'UNKWON')
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    current_user = models.ForeignKey(User, related_name="profile_user", on_delete=models.CASCADE)
    profile_type = models.CharField(choices=PROFILE_TYPE_CHOICES, max_length=1, default='U')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Stage(models.Model):
    USER_STAGE_CHOICES = (
        ('G', 'GRADUATED'),
        ('U', 'UNGRADUATED'),
        ('I', 'IN CLASS')
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    current_user = models.ForeignKey(User, related_name="stage_user", on_delete=models.CASCADE)
    user_stage = models.CharField(choices=USER_STAGE_CHOICES, max_length=1, default='I')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)