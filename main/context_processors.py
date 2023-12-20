from .models import ExtraUser

def profile_picture(request):
    if request.user.is_authenticated:
        profile = ExtraUser.objects.get(user=request.user)
        return {'profile_picture': profile.profile_picture}
    return {}