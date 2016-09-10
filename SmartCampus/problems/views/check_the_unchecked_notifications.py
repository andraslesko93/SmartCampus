from django.contrib.auth.decorators import login_required
from problems.models import UserProfile, Notification
from django.http.response import JsonResponse


@login_required
def check_the_unchecked_notifications(request):
    try:       
        unchecked_notifications = Notification.objects.filter(user__exact = request.user, 
                                                              status__exact="unchecked")         
    except UserProfile.DoesNotExist :
        pass
    for unchecked_notification in unchecked_notifications:
        unchecked_notification.status = "checked"
        unchecked_notification.save()
    return JsonResponse({'Response': 'All unchecked notifications has been setted to checked'})
