from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.ExamListAPIView.as_view(), name='list_exams'),
    url(r'^published/$', views.ExamListUserAPIView.as_view(), name='list_published_exams'),
    url(r'^create/$', views.ExamCreateAPIView.as_view(), name='create_exam'),
    url(r'^detail/(?P<pk>[0-9a-f-]+)/$', views.ExamRetrieveAPIView.as_view(), name='detail_exam'),
    url(r'^(?P<pk>[0-9a-f-]+)/update/$', views.ExamUpdateAPIView.as_view(), name='update_exam'),
    url(r'^(?P<pk>[0-9a-f-]+)/delete/$', views.ExamDestroyAPIView.as_view(), name='delete_exam'),

    url(r'^questions/$', views.QuestionListAPIView.as_view(), name='list_questions'),
    url(r'^question/create/$', views.QuestionCreateAPIView.as_view(), name='create_question'),
    url(r'^question/detail/(?P<pk>[0-9a-f-]+)/$', views.QuestionRetrieveAPIView.as_view(), name='detail_question'),
    url(r'^question/(?P<pk>[0-9a-f-]+)/delete/$', views.QuestionDestroyAPIView.as_view(), name='delete_question'),

    url(r'^responses/$', views.ResponseListAPIView.as_view(), name='list_responses'),
    url(r'^response/create/$', views.ResponseCreateAPIView.as_view(), name='create_response'),
    url(r'^response/(?P<pk>[0-9a-f-]+)/delete/$', views.ResponseDestroyAPIView.as_view(), name='delete_response'),

    url(r'^questions/status/$', views.QuestionStatusListAPIView.as_view(), name='list_questions_status'),
    url(r'^question/status/create/$', views.QuestionStatusCreateAPIView.as_view(), name='create_question_status'),
    url(r'^question/status/detail/(?P<pk>[0-9a-f-]+)/$', views.QuestionStatusRetrieveAPIView.as_view(), name='detail_question_status'),
    url(r'^question/status/(?P<pk>[0-9a-f-]+)/delete/$', views.QuestionStatusDestroyAPIView.as_view(), name='delete_question_status'),

    url(r'^marks/$', views.ExamMarksListAPIView.as_view(), name='list_marks'),
    url(r'^mark/create/$', views.ExamMarksCreateAPIView.as_view(), name='create_marks'),
    url(r'^marks/admin/$', views.ExamMarksAdminListAPIView.as_view(), name='admin_list_marks'),
]