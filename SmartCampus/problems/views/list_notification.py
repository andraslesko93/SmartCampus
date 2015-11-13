from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from problems.models import UserProfile, Notification


@login_required
def list_notification(request):
    try:       
        unchecked_notifications = Notification.objects.filter(user__exact = request.user, 
                                                              status__exact="unchecked")
        unchecked_notifications = unchecked_notifications.order_by('-timestamp')
        
        checked_notifications = Notification.objects.filter(user__exact = request.user, 
                                                              status__exact="checked")
        checked_notifications = checked_notifications.order_by('-timestamp')[:20]
        
    except UserProfile.DoesNotExist :
        pass
    
    for checked_notification in checked_notifications:
        pass
    
    for unchecked_notification in unchecked_notifications:
        unchecked_notification.status = "checked"
        unchecked_notification.save()
        
    request.user.userprofile.notification_number = 0
    request.user.userprofile.save()
    
    context_dict = {'unchecked_notifications': unchecked_notifications, 
                    'checked_notifications': checked_notifications}
    return render(request, 'problems/notification.html', context_dict)  
