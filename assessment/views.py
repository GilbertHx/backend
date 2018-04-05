from django.shortcuts import render
from .serializers import AssessmentSerializer, QuestionSerializer, ResponseSerializer, EssayResponseSerializer, EssayRatingSerializer, QuestionStatusSerializer, RetakeAssessmentSerializer, AssessmentMarksSerializer, AssessmentMarksAdminSerializer
from .models import Assessment, Question, Response, EssayResponse, EssayRating, QuestionStatus, AssessmentMarks
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Assessment
class AssessmentListAPIView(generics.ListAPIView):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer

class AssessmentRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer

class AssessmentCreateAPIView(generics.CreateAPIView):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    permission_classes = (IsAdminUser,)

class AssessmentDestroyAPIView(generics.DestroyAPIView):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
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

class ResponseRetrieveAPIView(generics.RetrieveAPIView):
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

# EssayResponse
class EssayResponseListAPIView(generics.ListAPIView):
    queryset = EssayResponse.objects.all()
    serializer_class = EssayResponseSerializer

class EssayResponseRetrieveAPIView(generics.RetrieveAPIView):
    queryset = EssayResponse.objects.all()
    serializer_class = EssayResponseSerializer

class EssayResponseCreateAPIView(generics.CreateAPIView):
    queryset = EssayResponse.objects.all()
    serializer_class = EssayResponseSerializer
    permission_classes = (IsAuthenticated,)

    # def get_queryset(self):
    #     user = self.request.user
    #     return EssayResponse.objects.filter(current_user=user)
    
    # def perform_create(self, serializer):
    #     if EssayResponse.objects.filter(current_user_id=self.request.user, question_id=serializer.data['question']).exists():
    #         EssayResponse.objects.filter(current_user_id=self.request.user, question_id=serializer.data['question']).update(essay=serializer.data['essay'])
    #     else:
    #         EssayResponse.objects.create(current_user_id=self.request.user.id, question_id=serializer.data['question'], essay=serializer.data['essay'])

class EssayResponseDestroyAPIView(generics.DestroyAPIView):
    queryset = EssayResponse.objects.all()
    serializer_class = EssayResponseSerializer

# QuestionStatus
class QuestionStatusListAPIView(generics.ListAPIView):
    queryset = QuestionStatus.objects.all()
    serializer_class = QuestionStatusSerializer

class QuestionStatusRetrieveAPIView(generics.RetrieveAPIView):
    queryset = QuestionStatus.objects.all()
    serializer_class = QuestionStatusSerializer

class RetakeAssessmentUpdateAPIView(generics.UpdateAPIView):
    queryset = Assessment.objects.all()
    serializer_class = RetakeAssessmentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        questions = Question.objects.filter(assessment_id=serializer.data['id'])

        for question in questions:
            QuestionStatus.objects.filter(question_id=question.id).update(done=False)
        # for question in questions:
        #     question.update(done=False)

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
            if serializer.data['done']:
                QuestionStatus.objects.create(current_user_id=self.request.user.id, question_id=serializer.data['question'], done=serializer.data['done'])
            else:
                QuestionStatus.objects.create(current_user_id=self.request.user.id, question_id=serializer.data['question'])

class QuestionStatusDestroyAPIView(generics.DestroyAPIView):
    queryset = QuestionStatus.objects.all()
    serializer_class = QuestionStatusSerializer
    permission_classes = (IsAuthenticated,)


# AssessmentMarks
class AssessmentMarksAdminListAPIView(generics.ListAPIView):
    queryset = AssessmentMarks.objects.all()
    serializer_class = AssessmentMarksAdminSerializer
    permission_classes = (IsAuthenticated,)

class AssessmentMarksListAPIView(generics.ListAPIView):
    serializer_class = AssessmentMarksSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return AssessmentMarks.objects.filter(current_user=user)

class AssessmentMarksRetrieveAPIView(generics.RetrieveAPIView):
    queryset = AssessmentMarks.objects.all()
    serializer_class = AssessmentMarksSerializer

class AssessmentMarksCreateAPIView(generics.CreateAPIView):
    queryset = AssessmentMarks.objects.all()
    serializer_class = AssessmentMarksSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        if AssessmentMarks.objects.filter(current_user_id=self.request.user, assessment_id=serializer.data['assessment']).exists():
            all_completed_questions = QuestionStatus.objects.filter(completed=True, current_user=self.request.user)
            marks = 0
            for q in all_completed_questions:
                if q.question.assessment.id == serializer.data['assessment']:
                    marks = marks + q.question.marks
            AssessmentMarks.objects.filter(current_user_id=self.request.user, assessment_id=serializer.data['assessment']).update(marks=marks)
        else:
            all_completed_questions = QuestionStatus.objects.filter(completed=True, current_user=self.request.user)
            marks = 0
            for q in all_completed_questions:
                if q.question.assessment.id == serializer.data['assessment']:
                    marks = q.question.marks
            AssessmentMarks.objects.create(current_user_id=self.request.user.id, assessment_id=serializer.data['assessment'],marks=marks)

    def get_queryset(self):
        user = self.request.user
        return AssessmentMarks.objects.filter(current_user=user)

class AssessmentMarksDestroyAPIView(generics.DestroyAPIView):
    queryset = AssessmentMarks.objects.all()
    serializer_class = AssessmentMarksSerializer