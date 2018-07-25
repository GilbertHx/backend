from django.shortcuts import render
from rest_auth.registration.views import RegisterView
from rest_framework.response import Response
from rest_framework import status
from .models import Stage, Certificate, Profile, UserComment
from rest_framework import generics, views
from django.contrib.auth.models import User
from .serializers import UserSerializer, StageSerializer, CertificateSerializer, CertificateCreateSerializer, ProfileSerializer, AdminStageSerializer, UserCommentSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from django.http import HttpResponse
from django.views.generic import View
from accounts.utils import make_pdf 
from django.template.loader import get_template

from django.core.files import File
# from django.core.files.temp import NamedTemporaryFile
from django.core.files.base import ContentFile
from xhtml2pdf import pisa
from datetime import datetime
from django.conf import settings
from easy_pdf.views import PDFTemplateView, PDFTemplateResponseMixin
import easy_pdf

from django.views.generic.base import TemplateView

class HelloPDFView(PDFTemplateView):
    template_name = "certificate.html"

    def get_context_data(self, **kwargs):
        return super(HelloPDFView, self).get_context_data(
            pagesize='A4 landscape',
            title='Hi there!',
            **kwargs
        )

class HomePageView(PDFTemplateResponseMixin, generics.ListCreateAPIView):
    serializer_class = CertificateCreateSerializer
    permission_classes = (IsAuthenticated,)
    template_name = "certificate.html"
    queryset = Certificate.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if Certificate.objects.filter(current_user=serializer.data['current_user']).exists():
            certificate = Certificate.objects.filter(current_user=serializer.data['current_user']).first()
            certificate_url = settings.DOMAIN_NAME + certificate.user_certificate.url
            session_dict = dict()
            session_dict['user_certificate'] = certificate_url

            headers = self.get_success_headers(serializer.data)
            return Response(session_dict, status=status.HTTP_200_OK, headers=headers)

        else:
            user_ = Profile.objects.filter(id=serializer.data['current_user']).first();
            template = get_template('certificate.html')
            context = {
                "user_first_name": user_.first_name,
                "user_last_name": user_.last_name,
            }
            
            # file_tmp = ContentFile(b"")
            # html  = template.render(context)
            pdf_cert = easy_pdf.rendering.render_to_pdf('certificate.html', context)

            import pdb;
            pdb.set_trace();
            certificate = Certificate(current_user=user_)
            certificate.save()
            certificate.user_certificate.save("certificate_%s.pdf" %certificate.id, ContentFile(pdf_cert))
            certificate.save()

            certificate_url = settings.DOMAIN_NAME + certificate.user_certificate.url
            session_dict = dict()
            session_dict['user_certificate'] = certificate_url

            headers = self.get_success_headers(serializer.data)
            return Response(session_dict, status=status.HTTP_201_CREATED, headers=headers)

    # base_url = 'file://' + settings.STATIC_URL
    # download_filename = 'invoice.pdf'

    def get_context_data(self, **kwargs):
        return super(HomePageView, self).get_context_data(
            pagesize='A4 landscape',
            title='Hi there!',
            **kwargs
        )

# User
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

# Profile
class ProfileUpdateAPIView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

# Stage
class StageListAPIView(generics.ListAPIView):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer

class AdminStageCreateAPIView(generics.CreateAPIView):
    serializer_class = AdminStageSerializer
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        if Stage.objects.filter(current_user_id=serializer.data['current_user']).exists():
            Stage.objects.filter(current_user_id=serializer.data['current_user']).update(user_stage=serializer.data['user_stage'])
        else:
            Stage.objects.create(current_user_id=serializer.data['current_user'], user_stage=serializer.data['user_stage'])

class StageCreateAPIView(generics.CreateAPIView):
    serializer_class = StageSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        if Stage.objects.filter(current_user_id=self.request.user.id).exists():
            Stage.objects.filter(current_user_id=self.request.user.id).update(user_stage=serializer.data['user_stage'])
        else:
            if serializer.data['user_stage']:
                Stage.objects.create(current_user_id=self.request.user.id, user_stage=serializer.data['user_stage'])
            Stage.objects.create(current_user_id=self.request.user.id)

    def get_queryset(self):
        user = self.request.user
        return Stage.objects.filter(current_user=user)

class StageUpdateAPIView(generics.UpdateAPIView):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer

class ListSummary(views.APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        summary_dict = dict()
        summary_dict['staff_number'] = User.objects.filter(is_staff=True, is_active=True).count()
        summary_dict['student_number'] = User.objects.filter(is_staff=False, is_active=True).count()
        summary_dict['graduates_number'] = Stage.objects.filter(user_stage=Stage.GRADUATED).count()
        summary_dict['ungraduates_number'] = Stage.objects.filter(user_stage=Stage.UNGRADUATED).count()
        summary_dict['still_learning_number'] = Stage.objects.filter(user_stage=Stage.IN_CLASS).count()
        return Response(summary_dict)

class CurrentUserView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# Create your views here.
class MyRegistrationView(RegisterView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        user.is_active = False
        user.save()
        Stage.objects.create(current_user_id=user.id, user_stage=Stage.NOT_STUDENT)
        headers = self.get_success_headers(serializer.data)

        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)

class CertificateListAPIView(generics.ListAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer

class CertificateCreateAPIView(generics.CreateAPIView):
    serializer_class = CertificateCreateSerializer
    permission_classes = (IsAuthenticated,)
    template_name = "certificate.html"

    def get_queryset(self):
        user = self.request.user
        return EssayResponse.objects.filter(current_user=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if Certificate.objects.filter(current_user=serializer.data['current_user']).exists():
            certificate = Certificate.objects.filter(current_user=serializer.data['current_user']).first()
            certificate_url = settings.DOMAIN_NAME + certificate.user_certificate.url
            session_dict = dict()
            session_dict['user_certificate'] = certificate_url

            headers = self.get_success_headers(serializer.data)
            return Response(session_dict, status=status.HTTP_200_OK, headers=headers)

        else:
            profile_ = Profile.objects.filter(id=serializer.data['current_user']).first();
            user_ = User.objects.filter(id=serializer.data['current_user']).first();
            template = get_template('certificate.html')
            context = {
                "user_first_name": profile_.first_name,
                "user_last_name": profile_.last_name,
                "reg_number": user_.username,
            }
            
            # file_tmp = ContentFile(b"")
            # html  = template.render(context)
            pdf_cert = easy_pdf.rendering.render_to_pdf('certificate.html', context)

            certificate = Certificate(current_user=user_)
            certificate.save()
            certificate.user_certificate.save("certificate_%s.pdf" %certificate.id, ContentFile(pdf_cert))
            certificate.save()

            certificate_url = settings.DOMAIN_NAME + certificate.user_certificate.url
            session_dict = dict()
            session_dict['user_certificate'] = certificate_url

            headers = self.get_success_headers(serializer.data)
            return Response(session_dict, status=status.HTTP_201_CREATED, headers=headers)

class CertificateDestroyAPIView(generics.DestroyAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateCreateSerializer
    permission_classes = (IsAdminUser,)

class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('certificate.html')
        context = {
            "invoice_id": 123,
            "customer_name": "John Cooper",
            "today": "Today",
        }
        html = template.render(context)
        pdf = make_pdf('certificate.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

class UserCommentListAPIView(generics.ListAPIView):
    queryset = UserComment.objects.all()
    serializer_class = UserCommentSerializer

class UserCommentRetrieveAPIView(generics.RetrieveAPIView):
    queryset = UserComment.objects.all()
    serializer_class = UserCommentSerializer

class UserCommentCreateAPIView(generics.CreateAPIView):
    queryset = UserComment.objects.all()
    serializer_class = UserCommentSerializer
    permission_classes = (IsAdminUser,)

class UserCommentDestroyAPIView(generics.DestroyAPIView):
    queryset = UserComment.objects.all()
    serializer_class = UserCommentSerializer
    permission_classes = (IsAdminUser,)