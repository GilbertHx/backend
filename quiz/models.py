import uuid
from django.db import models
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from course.models import Lesson

class Quiz(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    lesson = models.ForeignKey(Lesson, related_name="lesson_quiz", on_delete=models.CASCADE)
    label = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label

class Answer(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, related_name="quiz_answer", on_delete=models.CASCADE)
    label = models.TextField()
    correct = models.BooleanField(blank=False, default=False, help_text=("Is this a correct answer?"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label

class QuizComplete(models.Model):
    BOOLEAN_CHOICES = (
            (None,''),
            (True,'Yes'), 
            (False, 'No')
        )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    current_user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name="quiz_to_complete", on_delete=models.CASCADE)
    completed = models.NullBooleanField(choices=BOOLEAN_CHOICES, max_length=3,
                                    blank=True, null=True, default=None,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)