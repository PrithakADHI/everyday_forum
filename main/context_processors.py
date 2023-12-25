from .models import ExtraUser, Notification

from .forms import UserSearchForm

def profile_picture(request):
    if request.user.is_authenticated:
        profile = ExtraUser.objects.get(user=request.user)
        return {'profile_picture': profile.profile_picture}
    return {}

def notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).first()

        return {'notifications': notifications}
    return {}
