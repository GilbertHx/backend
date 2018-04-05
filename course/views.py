from django.shortcuts import render
from .serializers import UnitSerializer, SessionSerializer, LessonSerializer, LessonCompletedSerializer, LessonCompletionSerializer
from .models import Unit, Session, Lesson, LessonComplete
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Unit
class UnitListAPIView(generics.ListAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

class UnitRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

class UnitCreateAPIView(generics.CreateAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = (IsAdminUser,)

class UnitDestroyAPIView(generics.DestroyAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = (IsAdminUser,)

# Session
class SessionListAPIView(generics.ListAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

class SessionRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

class SessionCreateAPIView(generics.CreateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = (IsAdminUser,)

class SessionDestroyAPIView(generics.DestroyAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = (IsAdminUser,)

# Lesson
class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAdminUser,)

class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAdminUser,)

# LessonComplete
class LessonCompletedListAPIView(generics.ListAPIView):
    serializer_class = LessonCompletedSerializer

    def get_queryset(self):
        user = self.request.user
        return LessonComplete.objects.filter(current_user=user)

class LessonCompletedCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonCompletionSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        if LessonComplete.objects.filter(current_user_id=self.request.user, lesson_id=serializer.data['lesson']).exists():
            LessonComplete.objects.filter(current_user_id=self.request.user, lesson_id=serializer.data['lesson']).update(completed=serializer.data['completed'])
        else:
            LessonComplete.objects.create(current_user_id=self.request.user.id, lesson_id=serializer.data['lesson'],completed=serializer.data['completed'])

    def get_queryset(self):
        user = self.request.user
        return LessonComplete.objects.filter(current_user=user)