import uuid
from django.db import models
from django.contrib.auth.models import User
from course.models import Unit
# Create your models here.

def scramble_uploaded_filename(instance, filename):
    extension = filename.split(".")[-1]
    return "{}.{}".format(uuid.uuid4(), extension)

class Assessment(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    unit = models.ForeignKey(Unit, related_name="unit_assessment", on_delete=models.CASCADE)
    label = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label

class Question(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name="assessment_question")
    label = models.TextField()
    marks = models.PositiveSmallIntegerField(default=0)
    is_essay = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EssayResponse(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    current_user = models.ForeignKey(User, related_name="essay_user", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question_essay_response")
    title = models.CharField(max_length=255, blank=True, default='')
    essay = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Response(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question_response")
    label = models.TextField()
    correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EssayRating(models.Model):
    RATING_CHOICES = (
        (1, 'Poor'),
        (2, 'Average'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Excellent')
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    current_user = models.ForeignKey(User, related_name="rating_user", on_delete=models.CASCADE)
    essay = models.ForeignKey(EssayResponse, related_name="rated_essay", on_delete=models.CASCADE)
    comment = models.CharField(max_length=2550, blank=True, default='')
    rating = models.IntegerField(choices=RATING_CHOICES, default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class QuestionStatus(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    current_user = models.ForeignKey(User, related_name="assessment_question_user", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name="assessment_question_done", on_delete=models.CASCADE)
    done = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AssessmentMarks(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    current_user = models.ForeignKey(User, related_name="user_marks", on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name="assessment_marks")
    marks = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)