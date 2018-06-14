import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# class Profile(models.Model):
#     PROFILE_TYPE_CHOICES = (
#         ('R', 'REG'),
#         ('S', 'STUDENT'),
#         ('U', 'UNKWON')
#     )

#     uuid = models.UUIDField(default=uuid.uuid4, editable=False)
#     current_user = models.ForeignKey(User, related_name="profile_user", on_delete=models.CASCADE)
#     profile_type = models.CharField(choices=PROFILE_TYPE_CHOICES, max_length=1, default='U')
#     is_active = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

def scramble_uploaded_filename(instance, filename):
    extension = filename.split(".")[-1]
    return "{}.{}".format(uuid.uuid4(), extension)


class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True, default='')
    last_name = models.CharField(max_length=255, blank=True, default='')
    national_id_number = models.CharField(max_length=255, blank=True, default='')
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='F')
    province = models.CharField(max_length=255, blank=True, default='')
    district = models.CharField(max_length=255, blank=True, default='')
    sector = models.CharField(max_length=255, blank=True, default='')
    qualification = models.CharField(max_length=255, blank=True, default='')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Stage(models.Model):
    GRADUATED = 'G'
    UNGRADUATED = 'U'
    IN_CLASS = 'I'
    NOT_STUDENT = 'N'

    USER_STAGE_CHOICES = (
        (GRADUATED, 'GRADUATED'),
        (UNGRADUATED, 'UNGRADUATED'),
        (IN_CLASS, 'IN CLASS'),
        (NOT_STUDENT, 'NOT STUDENT')
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    current_user = models.ForeignKey(User, related_name="stage_user", on_delete=models.CASCADE)
    user_stage = models.CharField(choices=USER_STAGE_CHOICES, max_length=1, default='N')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Certificate(models.Model):
    current_user = models.ForeignKey(User, related_name="graduate_user", on_delete=models.CASCADE)
    user_certificate = models.FileField("Certificates", upload_to=scramble_uploaded_filename)
    created_at = models.DateTimeField(auto_now_add=True)
