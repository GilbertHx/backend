from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Assessment, Question, Response, EssayResponse, EssayRating, QuestionStatus, AssessmentMarks

class AssessmentSerializer(ModelSerializer):
    questions = serializers.SerializerMethodField()
    def get_questions(self, obj):
        l = []
        responses = Response.objects.values()
        done = QuestionStatus.objects.values()
        questions = obj.assessment_question.values()
        for q in questions:
            q['done'] = done.filter(question_id=q['id'])
            q['responses'] = responses.filter(question_id=q['id'])
            l.append(q)
        return l

    class Meta:
        model = Assessment
        fields = [
            'id',
            'uuid',
            'unit',
            'label',
            'questions',
        ]

class QuestionSerializer(ModelSerializer):
    done = serializers.SerializerMethodField()
    def get_done(self, obj):
        result = []
        all_q_done = obj.assessment_question_done.values()
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
            'assessment',
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

class EssayResponseSerializer(ModelSerializer):
    class Meta:
        model = EssayResponse
        fields = [
            'id',
            'uuid',
            'question',
            'essay',
        ]

class EssayRatingSerializer(ModelSerializer):
    class Meta:
        model = EssayRating
        fields = [
            'id',
            'uuid',
            'comment',
            'current_user',
            'essay',
            'rating',
        ]

class QuestionStatusSerializer(ModelSerializer):
    class Meta:
        model = QuestionStatus
        fields = [
            'id',
            'uuid',
            'question',
            'done',
            'completed'
        ]

class RetakeAssessmentSerializer(ModelSerializer):
    class Meta:
        model = Assessment
        fields = [
            'id',
        ]

class AssessmentMarksSerializer(ModelSerializer):
    class Meta:
        model = AssessmentMarks
        fields = [
            'id',
            'uuid',
            'assessment',
            'marks',
        ]

class AssessmentMarksAdminSerializer(ModelSerializer):
    class Meta:
        model = AssessmentMarks
        fields = [
            'id',
            'uuid',
            'current_user',
            'assessment',
            'marks',
        ]