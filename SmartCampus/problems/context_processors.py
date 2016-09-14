from types import NoneType
def daily_repu_out(request):
    from problems.views.support_functions import daily_reputation_counter, limit
    
    if (request.user.is_authenticated()):
        daily_reputation = daily_reputation_counter(request.user)
    else:
        daily_reputation = 0
    return {'daily_reputation': daily_reputation, 'limit': limit}

def rating_number_counter(request):
    from problems.models import Rating
   
    if (request.user.is_authenticated()):
        pending_ratings = Rating.objects.filter (user__exact = request.user, status__exact ="pending")
        rating_count = pending_ratings.count()
    else:
        rating_count = 0
    return {'rating_count': rating_count}

def notifications(request):
    from problems.models import Notification
    if (request.user.is_authenticated()):
        notifications = Notification.objects.filter(user__exact = request.user)
        notifications = notifications.order_by('-timestamp')
        notification_count = Notification.objects.filter(user__exact = request.user, status__exact="unchecked").count()
    else:
        notification_count = 0
        notifications = None
    return {'notifications': notifications,'notification_count' : notification_count}


def switch_rating_status (request):
    from problems.models import Rating
    from django.utils import timezone
    from datetime import timedelta
    now = timezone.now()
    dummy =""
    if (request.user.is_authenticated()): 
        try:
            waiting_ratings = Rating.objects.filter(user__exact = request.user, status__exact = "waiting")
        except Rating.DoesNotExist:
            pass
        now = now + timezone.timedelta(0, 60)
        for waiting_rating in waiting_ratings:    
            if (now >= (waiting_rating.solution.problem_id.deadline + timedelta(seconds = 3600))):
                waiting_rating.status = "pending"
                waiting_rating.save()
                
    return {'dummy':dummy, 'now': now}

def tag_cloud(request):
    from problems.views.support_functions import tag_cloud
    tags = tag_cloud()
    return {'tags':tags}
