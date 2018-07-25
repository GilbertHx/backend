from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Stage, Certificate, Profile, UserComment
from django.conf import settings

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id',
            'first_name',
            'last_name',
            'national_id_number',
            'birth_date',
            'gender',
            'province',
            'district',
            'sector',
            'qualification',
        ]

class UserCommentSerializer(ModelSerializer):
    class Meta:
        model = UserComment
        fields = [
            'id',
            'current_user',
            'comment',
            'created_at',
        ]

class UserSerializer(ModelSerializer):
    
    stage = serializers.SerializerMethodField()
    def get_stage(self, obj):
        return obj.stage_user.values()
    
    profile = ProfileSerializer(read_only=True)
    
    comments = serializers.SerializerMethodField()
    def get_comments(self, obj):
        return obj.user_commeted.values()

    assessment_marks = serializers.SerializerMethodField()
    def get_assessment_marks(self, obj):
        output = []
        assessment_marks = obj.user_marks.all()
        for mark in assessment_marks:
            marks_dict = dict()
            marks_dict['id'] = mark.id
            marks_dict['uuid'] = mark.uuid
            marks_dict['assessment'] = mark.assessment_id
            marks_dict['assessment_title'] = mark.assessment.label
            marks_dict['marks'] = mark.marks
            output.append(marks_dict)
        return output
    
    exam_marks = serializers.SerializerMethodField()
    def get_exam_marks(self, obj):
        output = []
        exam_marks = obj.user_exam_marks.all()
        for mark in exam_marks:
            marks_dict = dict()
            marks_dict['id'] = mark.id
            marks_dict['uuid'] = mark.uuid
            marks_dict['exam'] = mark.exam_id
            marks_dict['exam_title'] = mark.exam.title
            marks_dict['marks'] = mark.marks
            output.append(marks_dict)
        return output
    
    certificate = serializers.SerializerMethodField()
    def get_certificate(self, obj):
        certificate = obj.graduate_user.first()
        if certificate:
            cert_dict = dict()
            cert_dict['id'] = certificate.id
            cert_dict['url'] = settings.DOMAIN_NAME + certificate.user_certificate.url
            return cert_dict
        return

    essay_submitted = serializers.SerializerMethodField()
    def get_essay_submitted(self, obj):
        return obj.essay_user.values()
    
    reviews_made = serializers.SerializerMethodField()
    def get_reviews_made(self, obj):
        return obj.rating_user.values()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'is_active',
            'is_staff',
            'first_name',
            'last_name',
            'email',
            'is_superuser',
            'certificate',
            'profile',
            'comments',
            'stage',
            'assessment_marks',
            'exam_marks',
            'essay_submitted',
            'reviews_made',
        ]
        read_only_fields = ('id', 'username', 'email', 'is_superuser')

class StageSerializer(ModelSerializer):
    class Meta:
        model = Stage
        fields = [
            'user_stage',
        ]

class AdminStageSerializer(ModelSerializer):
    class Meta:
        model = Stage
        fields = [
            'current_user',
            'user_stage',
        ]

class CertificateSerializer(ModelSerializer):
    class Meta:
        model = Certificate
        fields = [
            'id',
            'current_user',
            'user_certificate',
            'created_at'
        ]

class CertificateCreateSerializer(ModelSerializer):
    class Meta:
        model = Certificate
        fields = [
            'current_user',
            'user_certificate',
        ]

        read_only_fields= [
            'user_certificate'
        ]