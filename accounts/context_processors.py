# from .models import Profile

# def profile_processor(request):
#     profile = None

#     if hasattr(request, 'user') and request.user.is_authenticated():
#         profile = Profile.objects.filter(current_user=request.user).first()

#     if profile:
#         return dict(profile=profile)
#     return dict()