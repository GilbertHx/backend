from django.shortcuts import render
from .serializers import QuizSerializer, QuizCompleteSerializer, AnswerSerializer
from .models import Quiz, Answer, QuizComplete
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class QuizListAPIView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuizRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuizCreateAPIView(generics.CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuizDestroyAPIView(generics.DestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuizCompletionListAPIView(generics.ListAPIView):
    serializer_class = QuizCompleteSerializer

    def get_queryset(self):
        user = self.request.user
        return QuizComplete.objects.filter(current_user=user)

class QuizCompletionCreateAPIView(generics.CreateAPIView):
    serializer_class = QuizCompleteSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        if QuizComplete.objects.filter(current_user_id=self.request.user, quiz_id=serializer.data['quiz']).exists():
            QuizComplete.objects.filter(current_user_id=self.request.user, quiz_id=serializer.data['quiz']).update(completed=serializer.data['completed'])
        else:
            QuizComplete.objects.create(current_user_id=self.request.user.id, quiz_id=serializer.data['quiz'],completed=serializer.data['completed'])

    def get_queryset(self):
        user = self.request.user
        return QuizComplete.objects.filter(current_user=user)

class AnswerListAPIView(generics.ListAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class AnswerCreateAPIView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer