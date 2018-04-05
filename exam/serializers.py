from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Exam, Question, Response, QuestionStatus, ExamMarks

class ExamSerializer(ModelSerializer):
    questions = serializers.SerializerMethodField()
    def get_questions(self, obj):
        l = []
        responses = Response.objects.values()
        questions = obj.exam_question.values()
        for q in questions:
            q['responses'] = responses.filter(question_id=q['id'])
            l.append(q)
        return l
    class Meta:
        model = Exam
        fields = [
            'id',
            'uuid',
            'title',
            'published',
            'questions',
        ]

class PublishingExamSerializer(ModelSerializer):
    class Meta:
        model = Exam
        fields = [
            'id',
            'uuid',
            'title',
            'published',
        ]

class QuestionSerializer(ModelSerializer):
    done = serializers.SerializerMethodField()
    def get_done(self, obj):
        result = []
        all_q_done = obj.question_done.values()
        for q_done in all_q_done:
            if q_done['current_user_id'] == self.context['request'].user.id:
                result.append(q_done)
        return result

    responses = serializers.SerializerMethodField()
    def get_responses(self, obj):
        return obj.question_response.values()

    class Meta:
        model = Question
        fields = [
            'id',
            'uuid',
            'exam',
            'label',
            'marks',
            'done',
            'responses',
        ]

class ResponseSerializer(ModelSerializer):
    class Meta:
        model = Response
        fields = [
            'id',
            'uuid',
            'question',
            'label',
            'correct',
        ]

class QuestionStatusSerializer(ModelSerializer):
    class Meta:
        model = QuestionStatus
        fields = [
            'id',
            'uuid',
            'question',
            'done',
            'completed',
        ]

class ExamMarksSerializer(ModelSerializer):
    class Meta:
        model = ExamMarks
        fields = [
            'id',
            'uuid',
            'exam',
            'marks',
        ]

class ExamMarksAdminSerializer(ModelSerializer):
    class Meta:
        model = ExamMarks
        fields = [
            'id',
            'uuid',
            'current_user',
            'exam',
            'marks',
        ]