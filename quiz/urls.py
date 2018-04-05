from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^create/$', views.QuizCreateAPIView.as_view(), name='create_quiz'),
    url(r'^list/$', views.QuizListAPIView.as_view(), name='list_quizzes'),
    url(r'^detail/(?P<pk>[0-9a-f-]+)/$', views.QuizRetrieveAPIView.as_view(), name='detail_quiz'),
    url(r'^(?P<pk>[0-9a-f-]+)/delete/$', views.QuizDestroyAPIView.as_view(), name='delete_quiz'),

    url(r'^completed/create/$', views.QuizCompletionCreateAPIView.as_view(), name='create_quiz_completion'),
    url(r'^completed/list/$', views.QuizCompletionListAPIView.as_view(), name='list_completed_quizzes'),

    url(r'^answer/create/$', views.AnswerCreateAPIView.as_view(), name='create_answer'),
    url(r'^answers/$', views.AnswerListAPIView.as_view(), name='list_answers'),
]