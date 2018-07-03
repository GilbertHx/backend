from django.shortcuts import render
from .serializers import ExamSerializer, PublishingExamSerializer, QuestionSerializer, ResponseSerializer, QuestionStatusSerializer, ExamMarksSerializer, ExamMarksAdminSerializer
from .models import  Exam, Question, Response, QuestionStatus, ExamMarks
from accounts.models import Stage
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Exam
class ExamListAPIView(generics.ListAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class ExamListUserAPIView(generics.ListAPIView):
    serializer_class = ExamSerializer

    def get_queryset(self):
        return Exam.objects.filter(published=True)

class ExamAdminRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = (IsAdminUser,)

class ExamRetrieveAPIView(generics.RetrieveAPIView):
    # queryset = Exam.objects.all()
    serializer_class = ExamSerializer

    def get_queryset(self):
        return Exam.objects.filter(published=True)

class ExamCreateAPIView(generics.CreateAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = (IsAdminUser,)

class ExamUpdateAPIView(generics.UpdateAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

    def perform_update(self, serializer):
        exams = Exam.objects.all()

        for exam in exams:
            Exam.objects.filter(id=exam.id).update(published=False)

        serializer.save()

class ExamDestroyAPIView(generics.DestroyAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = (IsAdminUser,)

# Question
class QuestionListAPIView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuestionRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuestionCreateAPIView(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminUser,)

class QuestionDestroyAPIView(generics.DestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminUser,)

# Response
class ResponseListAPIView(generics.ListAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

class ResponseCreateAPIView(generics.CreateAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = (IsAdminUser,)

class ResponseDestroyAPIView(generics.DestroyAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = (IsAdminUser,)

# QuestionStatus
class QuestionStatusListAPIView(generics.ListAPIView):
    queryset = QuestionStatus.objects.all()
    serializer_class = QuestionStatusSerializer

class QuestionStatusRetrieveAPIView(generics.RetrieveAPIView):
    queryset = QuestionStatus.objects.all()
    serializer_class = QuestionStatusSerializer

class QuestionStatusCreateAPIView(generics.CreateAPIView):
    serializer_class = QuestionStatusSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return QuestionStatus.objects.filter(current_user=user)
    
    def perform_create(self, serializer):
        if QuestionStatus.objects.filter(current_user_id=self.request.user, question_id=serializer.data['question']).exists():
            QuestionStatus.objects.filter(current_user_id=self.request.user, question_id=serializer.data['question']).update(done=serializer.data['done'], completed=serializer.data['completed'])
        else:
            if serializer.data['done'] or serializer.data['completed']:
                QuestionStatus.objects.create(current_user_id=self.request.user.id, question_id=serializer.data['question'], done=serializer.data['done'], completed=serializer.data['completed'])
            else:
                QuestionStatus.objects.create(current_user_id=self.request.user.id, question_id=serializer.data['question'])

class QuestionStatusDestroyAPIView(generics.DestroyAPIView):
    queryset = QuestionStatus.objects.all()
    serializer_class = QuestionStatusSerializer
    permission_classes = (IsAuthenticated,)

# Marks
class ExamMarksAdminListAPIView(generics.ListAPIView):
    queryset = ExamMarks.objects.all()
    serializer_class = ExamMarksAdminSerializer
    permission_classes = (IsAuthenticated,)

class ExamMarksListAPIView(generics.ListAPIView):
    serializer_class = ExamMarksSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return ExamMarks.objects.filter(current_user=user)

class ExamMarksCreateAPIView(generics.CreateAPIView):
    serializer_class = ExamMarksSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        if ExamMarks.objects.filter(current_user_id=self.request.user, exam_id=serializer.data['exam']).exists():
            all_completed_questions = QuestionStatus.objects.filter(completed=True, current_user=self.request.user)
            all_question = QuestionStatus.objects.filter(current_user=self.request.user)
            marks = 0
            totalMarks = 0
            for q in all_completed_questions:
                if q.question.exam.id == serializer.data['exam']:
                    marks = marks + q.question.marks
            for q in all_question:
                if q.question.exam.id == serializer.data['exam']:
                    totalMarks = totalMarks + q.question.marks
            percentage_marks = 100 * (marks / totalMarks)
            if Stage.objects.filter(current_user=self.request.user, user_stage=Stage.IN_CLASS).exists():
                Stage.objects.filter(current_user=self.request.user, user_stage=Stage.IN_CLASS).update(user_stage=Stage.UNGRADUATED)
            ExamMarks.objects.filter(current_user_id=self.request.user, exam_id=serializer.data['exam']).update(marks=percentage_marks)
        else:
            all_completed_questions = QuestionStatus.objects.filter(completed=True, current_user=self.request.user)
            all_question = QuestionStatus.objects.filter(current_user=self.request.user)
            marks = 0
            totalMarks = 0
            for q in all_completed_questions:
                if q.question.exam.id == serializer.data['exam']:
                    marks = marks + q.question.marks
            for q in all_question:
                if q.question.exam.id == serializer.data['exam']:
                    totalMarks = totalMarks + q.question.marks
            percentage_marks = 100 * (marks / totalMarks)
            if Stage.objects.filter(current_user=self.request.user, user_stage=Stage.IN_CLASS).exists():
                Stage.objects.filter(current_user=self.request.user, user_stage=Stage.IN_CLASS).update(user_stage=Stage.UNGRADUATED)
            ExamMarks.objects.create(current_user_id=self.request.user.id, exam_id=serializer.data['exam'],marks=percentage_marks)

    def get_queryset(self):
        user = self.request.user
        return ExamMarks.objects.filter(current_user=user)