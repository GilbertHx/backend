import uuid
from django.db import models
from django.contrib.auth.models import User

class Exam(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True, default='')
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Question(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="exam_question")
    label = models.TextField()
    marks = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Response(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question_response")
    label = models.TextField()
    correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class QuestionStatus(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    current_user = models.ForeignKey(User, related_name="exam_question_user", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name="question_done", on_delete=models.CASCADE)
    done = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ExamMarks(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    current_user = models.ForeignKey(User, related_name="user_exam_marks", on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="exam_marks")
    marks = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)