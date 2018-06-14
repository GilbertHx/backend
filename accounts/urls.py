from django.conf.urls import url, include
from django.views.generic import TemplateView
from . import views
from rest_auth.registration.views import VerifyEmailView

urlpatterns = [
    url(r'^users/$', views.UserListAPIView.as_view(), name='list_users'),
    url(r'^user/detail/(?P<pk>[0-9a-f-]+)/$', views.UserRetrieveAPIView.as_view(), name='detail_user'),
    url(r'^user/(?P<pk>[0-9a-f-]+)/update/$', views.UserUpdateAPIView.as_view(), name='update_user'),
    url(r'^current/user/', views.CurrentUserView.as_view(), name='current_user'),

    url(r'^profile/(?P<pk>[0-9a-f-]+)/update/$', views.ProfileUpdateAPIView.as_view(), name='update_profile'),

    url(r'user/list/stage/$', views.StageListAPIView.as_view(), name='list_stage'),
    url(r'user/create/stage/$', views.StageCreateAPIView.as_view(), name='create_stage'),
    url(r'user/admin/create/stage/$', views.AdminStageCreateAPIView.as_view(), name='create_stage'),
    url(r'user/(?P<pk>[0-9a-f-]+)/update/stage/$', views.StageUpdateAPIView.as_view(), name='update_stage'),
    
    url(r'summary/', views.ListSummary.as_view(), name='summary'),

    url(r'^registration/$', views.MyRegistrationView.as_view(), name='rest_register'),
    url(r'^registration/verify-email/$', VerifyEmailView.as_view(), name='rest_verify_email'),
    # url(r'^pdf/$', views.GeneratePDF.as_view()),
    
    url(r'^certificates/$', views.CertificateListAPIView.as_view(), name='list_certificates'),
    url(r'^certificate/generate/$', views.CertificateCreateAPIView.as_view(), name='create_certificate'),
    url(r'^certificate/delete/(?P<pk>[0-9a-f-]+)/$', views.CertificateDestroyAPIView.as_view(), name='delete_certificate'),

    # This url is used by django-allauth and empty TemplateView is
    # defined just to allow reverse() call inside app, for example when email
    # with verification link is being sent, then it's required to render email
    # content.

    # account_confirm_email - You should override this view to handle it in
    # your API client somehow and then, send post to /verify-email/ endpoint
    # with proper key.
    # If you don't want to use API on that step, then just use ConfirmEmailView
    # view from:
    # django-allauth https://github.com/pennersr/django-allauth/blob/master/allauth/account/views.py
    url(r'^registration/account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(),
        name='account_confirm_email'),
]