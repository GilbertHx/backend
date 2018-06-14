# from .models import Profile

# class ProfileMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
#         profile = None

#         if hasattr(request, 'user') and request.user.is_authenticated:
#             profile = Profile.objects.filter(current_user=request.user).first()

#         import pdb; pdb.set_trace()
#         response.profile = profile
            
#         return response