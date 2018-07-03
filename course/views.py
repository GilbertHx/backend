from django.shortcuts import render
from .serializers import UnitSerializer, SessionSerializer, LessonSerializer, LessonCompletedSerializer, LessonCompletionSerializer, UnitAssessmentCompletedSerializer, UnitAssessmentCompletedCreateSerializer
from .models import Unit, Session, Lesson, LessonComplete, UnitAssessmentCompleted
from accounts.models import Stage
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from assessment.models import Assessment, AssessmentMarks

# Unit
class UnitListAPIView(generics.ListAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

class UnitRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

class UnitUpdateAPIView(generics.UpdateAPIView):
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

# Unit Assesment Complete
class UnitAssessmentCompletedListAPIView(generics.ListAPIView):
    queryset = UnitAssessmentCompleted.objects.all()
    serializer_class = UnitAssessmentCompletedSerializer

class UnitAssessmentCompletedCreateAPIView(generics.CreateAPIView):
    serializer_class = UnitAssessmentCompletedCreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        loop = 0
        units = Unit.objects.all()
        previous_is_completed = True
        for unit in units:
            if UnitAssessmentCompleted.objects.filter(current_user=self.request.user, unit_id=unit.id).exists():
                _unitAssessmentComplete = UnitAssessmentCompleted.objects.filter(current_user=self.request.user, unit_id=unit.id)

                _assessment = Assessment.objects.filter(unit_id=unit.id)
                for a in _assessment:
                    _assessment_marks_obj = AssessmentMarks.objects.filter(current_user=self.request.user, assessment_id=_assessment[0].id)
                    if _assessment_marks_obj.count() == 1:
                        for obj in _assessment_marks_obj:
                            _assessment_marks = obj.marks
                            if _assessment_marks > 59:
                                _unitAssessmentComplete.update(completed=True, show_unit=previous_is_completed)
                                previous_is_completed = True
                            else:
                                _unitAssessmentComplete.update(completed=False, show_unit=previous_is_completed)
                                previous_is_completed = False
                    else:
                        _unitAssessmentComplete.update(completed=False, show_unit=previous_is_completed)
                        previous_is_completed = False


            else:
                _assessment = Assessment.objects.filter(unit_id=unit.id)
                for a in _assessment:
                    _assessment_marks_obj = AssessmentMarks.objects.filter(current_user=self.request.user, assessment_id=_assessment[0].id)
                    if _assessment_marks_obj.count() == 1:
                        for obj in _assessment_marks_obj:
                            _assessment_marks = obj.marks
                            if _assessment_marks > 59:
                                UnitAssessmentCompleted.objects.create(current_user=self.request.user, unit_id=unit.id, completed=True, show_unit=previous_is_completed)
                                previous_is_completed = True
                            else:
                                UnitAssessmentCompleted.objects.create(current_user=self.request.user, unit_id=unit.id, completed=False, show_unit=previous_is_completed)
                                previous_is_completed = False
                    else:
                        UnitAssessmentCompleted.objects.create(current_user=self.request.user, unit_id=unit.id, completed=False, show_unit=previous_is_completed)
                        previous_is_completed = False

            loop =+ 1

    def get_queryset(self):
        user = self.request.user
        return LessonComplete.objects.filter(current_user=user)

class UnitAssessmentCompletedDestroyAPIView(generics.DestroyAPIView):
    queryset = UnitAssessmentCompleted.objects.all()
    serializer_class = UnitAssessmentCompletedSerializer
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

class SessionUpdateAPIView(generics.UpdateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

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

class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

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
        if LessonComplete.objects.filter(current_user=self.request.user, lesson_id=serializer.data['lesson']).exists():
            LessonComplete.objects.filter(current_user=self.request.user, lesson_id=serializer.data['lesson']).update(completed=serializer.data['completed'])
        else:
            if Stage.objects.filter(current_user=self.request.user, user_stage=Stage.NOT_STUDENT).exists():
                Stage.objects.filter(current_user=self.request.user, user_stage=Stage.NOT_STUDENT).update(user_stage=Stage.IN_CLASS)
            LessonComplete.objects.create(current_user=self.request.user, lesson_id=serializer.data['lesson'],completed=serializer.data['completed'])

    def get_queryset(self):
        user = self.request.user
        return LessonComplete.objects.filter(current_user=user)