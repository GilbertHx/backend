from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import  Quiz, Answer, QuizComplete

class QuizSerializer(ModelSerializer):
    answers = serializers.SerializerMethodField()
    def get_answers(self, obj):
        return obj.quiz_answer.values()
    
    lesson_title = serializers.SerializerMethodField()
    def get_lesson_title(self, obj):
        return obj.lesson.title

    class Meta:
        model = Quiz
        fields = [
            'id',
            'lesson',
            'label',
            'answers',
            'lesson_title',
        ]

class QuizCompleteSerializer(ModelSerializer):

    class Meta:
        model = QuizComplete
        fields = [
            'quiz',
            'completed',
        ]

class AnswerSerializer(ModelSerializer):

    class Meta:
        model = Answer
        fields = [
            'id',
            'quiz',
            'label',
            'correct',
        ]