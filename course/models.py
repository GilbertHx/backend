import uuid
from django.db import models
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
# Create your models here.

def scramble_uploaded_filename(instance, filename):
    extension = filename.split(".")[-1]
    return "{}.{}".format(uuid.uuid4(), extension)

class Unit(models.Model):
    """Entire single unit"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Session(models.Model):
    """Entire single session"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="unit_sessions")
    image = models.ImageField("Uploaded image", upload_to=scramble_uploaded_filename)
    title = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Lesson(models.Model):
    """A single Lesson in a session"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True, default='')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="session_lessons")
    description = models.TextField()
    lesson_index = models.PositiveSmallIntegerField()
    content = models.TextField()
    audio = models.FileField("Uploaded Audio", upload_to=scramble_uploaded_filename)
    video_url = models.CharField(max_length=1000, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class LessonComplete(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    current_user = models.ForeignKey(User, related_name="user_who_complete", on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name="lesson_to_complete", on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


