from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Unit, Session, Lesson, LessonComplete
from quiz.models import Answer
from django.conf import settings

class UnitSerializer(ModelSerializer):
    sessions = serializers.SerializerMethodField()
    def get_sessions(self, obj):
        output = []
        sessions = obj.unit_sessions.all()
        for session in sessions:
            session_dict = dict()
            session_dict['id'] = session.id
            session_dict['uuid'] = session.uuid
            session_dict['unit'] = session.unit_id
            session_dict['title'] = session.title
            session_dict['description'] = session.description
            session_dict['image'] = settings.DOMAIN_NAME + session.image.url
            output.append(session_dict)
        return output

    assessments = serializers.SerializerMethodField()
    def get_assessments(self, obj):
        return obj.unit_assessment.values()

    class Meta:
        model = Unit
        fields = [
            'id',
            'title',
            'description',
            'sessions',
            'assessments',
        ]

class SessionSerializer(ModelSerializer):
    lessons = serializers.SerializerMethodField()
    def get_lessons(self, obj):
        output = []
        lessions = obj.session_lessons.all()
        for lesson in lessions:
            lesson_dict = dict()
            lesson_dict['id'] = lesson.id
            lesson_dict['uuid'] = lesson.uuid
            lesson_dict['title'] = lesson.title
            # lesson_dict['session'] = dict(id=lesson.session.id, title=lesson.session.title)
            lesson_dict['session'] = lesson.session_id
            lesson_dict['description'] = lesson.description
            lesson_dict['lesson_index'] = lesson.lesson_index
            lesson_dict['content'] = lesson.content
            if lesson.audio:
                lesson_dict['audio'] = settings.DOMAIN_NAME + lesson.audio.url
            lesson_dict['video_url'] = lesson.video_url
            output.append(lesson_dict)
        return output
        
    class Meta:
        model = Session
        fields = [
            'id',
            'unit',
            'image',
            'title',
            'description',
            'lessons',
        ]

class LessonSerializer(ModelSerializer):
    quizzes = serializers.SerializerMethodField()
    def get_quizzes(self, obj):
        l = []
        answers = Answer.objects.values()
        quizzes = obj.lesson_quiz.values()
        
        for q in quizzes:
            q['answers'] = answers.filter(quiz_id=q['id'])
            l.append(q)
        return l

    class Meta:
        model = Lesson
        fields = [
            'id',
            'title',
            'session',
            'description',
            'lesson_index',
            'content',
            'audio',
            'video_url',
            'quizzes',
        ]

class LessonCompletionSerializer(ModelSerializer):

    class Meta:
        model = LessonComplete
        fields = [
            'lesson',
            'completed',
        ]

class LessonCompletedSerializer(ModelSerializer):

    class Meta:
        model = LessonComplete
        fields = [
            'current_user',
            'lesson',
            'completed',
        ]