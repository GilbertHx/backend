from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^unit/(?P<pk>[0-9a-f-]+)/delete/', views.UnitDestroyAPIView.as_view(), name='delete_unit'),
    url(r'^unit/create/', views.UnitCreateAPIView.as_view(), name='create_unit'),
    url(r'^unit/detail/(?P<pk>[0-9a-f-]+)', views.UnitRetrieveAPIView.as_view(), name='detail_unit'),
    url(r'^units/', views.UnitListAPIView.as_view(), name='list_units'),

    url(r'^session/(?P<pk>[0-9a-f-]+)/delete/', views.SessionDestroyAPIView.as_view(), name='delete_session'),
    url(r'^session/create/', views.SessionCreateAPIView.as_view(), name='create_session'),
    url(r'^session/detail/(?P<pk>[0-9a-f-]+)', views.SessionRetrieveAPIView.as_view(), name='detail_session'),
    url(r'^sessions/', views.SessionListAPIView.as_view(), name='list_sessions'),

    url(r'^lesson/(?P<pk>[0-9a-f-]+)/delete/', views.LessonDestroyAPIView.as_view(), name='delete_lesson'),
    url(r'^lesson/create/', views.LessonCreateAPIView.as_view(), name='create_lesson'),
    url(r'^lesson/detail/(?P<pk>[0-9a-f-]+)', views.LessonRetrieveAPIView.as_view(), name='detail_lesson'),
    url(r'^lessons/', views.LessonListAPIView.as_view(), name='list_lessons'),

    url(r'^completed/lesson/create/', views.LessonCompletedCreateAPIView.as_view(), name='create_completed_lesson'),
    url(r'^completed/lessons/', views.LessonCompletedListAPIView.as_view(), name='list_completed_lessons'),
]