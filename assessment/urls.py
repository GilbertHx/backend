from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.AssessmentListAPIView.as_view(), name='list_assessments'),
    url(r'^create/$', views.AssessmentCreateAPIView.as_view(), name='create_assessment'),
    url(r'^detail/(?P<pk>[0-9a-f-]+)/$', views.AssessmentRetrieveAPIView.as_view(), name='detail_assessment'),
    url(r'^(?P<pk>[0-9a-f-]+)/delete/$', views.AssessmentDestroyAPIView.as_view(), name='delete_assessment'),

    url(r'^questions/$', views.QuestionListAPIView.as_view(), name='list_questions'),
    url(r'^question/create/$', views.QuestionCreateAPIView.as_view(), name='create_question'),
    url(r'^question/detail/(?P<pk>[0-9a-f-]+)/$', views.QuestionRetrieveAPIView.as_view(), name='detail_question'),
    url(r'^question/(?P<pk>[0-9a-f-]+)/delete/$', views.QuestionDestroyAPIView.as_view(), name='delete_question'),

    url(r'^responses/$', views.ResponseListAPIView.as_view(), name='list_responses'),
    url(r'^response/create/$', views.ResponseCreateAPIView.as_view(), name='create_response'),
    url(r'^response/(?P<pk>[0-9a-f-]+)/delete/$', views.ResponseDestroyAPIView.as_view(), name='delete_response'),

    url(r'essay/responses/$', views.EssayResponseListAPIView.as_view(), name='list_essays'),
    url(r'^essay/response/create/$', views.EssayResponseCreateAPIView.as_view(), name='create_essay_response'),
    url(r'^essay/response/(?P<pk>[0-9a-f-]+)/delete/$', views.EssayResponseDestroyAPIView.as_view(), name='delete_essay_response'),
    url(r'^essay/response/detail/(?P<pk>[0-9a-f-]+)/$', views.EssayResponseRetrieveAPIView.as_view(), name='detail_essay_response'),

    url(r'essay/rates/$', views.EssayRatingListAPIView.as_view(), name='list_rates'),
    url(r'^essay/rate/create/$', views.EssayRatingCreateAPIView.as_view(), name='create_essay_rate'),
    url(r'^essay/rate/(?P<pk>[0-9a-f-]+)/delete/$', views.EssayRatingDestroyAPIView.as_view(), name='delete_rate_response'),

    url(r'^questions/status/$', views.QuestionStatusListAPIView.as_view(), name='list_questions_status'),
    url(r'^question/status/create/$', views.QuestionStatusCreateAPIView.as_view(), name='create_question_status'),
    url(r'^question/status/detail/(?P<pk>[0-9a-f-]+)/$', views.QuestionStatusRetrieveAPIView.as_view(), name='detail_question_status'),
    url(r'^question/status/(?P<pk>[0-9a-f-]+)/delete/$', views.QuestionStatusDestroyAPIView.as_view(), name='delete_question_status'),
    
    url(r'^(?P<pk>[0-9a-f-]+)/retake/$', views.RetakeAssessmentUpdateAPIView.as_view(), name='retake_assessment'),

    url(r'^marks/$', views.AssessmentMarksListAPIView.as_view(), name='list_marks'),
    url(r'^mark/create/$', views.AssessmentMarksCreateAPIView.as_view(), name='create_marks'),
    url(r'^marks/admin/$', views.AssessmentMarksAdminListAPIView.as_view(), name='admin_list_marks'),

    url(r'^essay/response/create/$', views.EssayResponseCreateAPIView.as_view(), name='create_essay_response'),
]