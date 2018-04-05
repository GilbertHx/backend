from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(ModelSerializer):
    profile = serializers.SerializerMethodField()
    def get_profile(self, obj):
        return obj.profile_user.values()
    
    assessment_marks = serializers.SerializerMethodField()
    def get_assessment_marks(self, obj):
        return obj.user_marks.values()
    
    exam_marks = serializers.SerializerMethodField()
    def get_exam_marks(self, obj):
        return obj.user_exam_marks.values()
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
            'profile',
            'assessment_marks',
            'exam_marks',
        ]
        read_only_fields = ('id', 'username', 'email', 'is_superuser')