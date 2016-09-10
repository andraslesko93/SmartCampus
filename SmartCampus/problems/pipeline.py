from .models import UserProfile
from problems.models import Notification
from django.contrib.contenttypes.models import ContentType

def create_user_profile(backend, user, response, details, *args, **kwargs):
    user_profile_match=UserProfile.objects.filter(user=user)
    if (user_profile_match.count()>0):
        return
    if backend.name == 'facebook':
        picture  = 'http://graph.facebook.com/{0}/picture?width=100'.format(response['id'])
        profile = UserProfile(user=user, picture_url=picture)
        profile.save()
        welcome_notification = Notification(user = user,
                                                content_type = ContentType.objects.get_for_model(user)
                                                )
        welcome_notification.save()