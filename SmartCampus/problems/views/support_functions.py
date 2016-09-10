
limit = 200

def reputation_adder(user, reputation):    
    if (reputation <0):
        if (user.userprofile.reputation + reputation < 0):
            return
        user.userprofile.reputation += reputation
        user.userprofile.save()
        return
    else:
        daily_reputation = daily_reputation_counter(user)
        if (daily_reputation >= limit):
            return        
        if (daily_reputation + reputation >= limit ):
            user.userprofile.reputation += (limit - daily_reputation)
        else:
            user.userprofile.reputation += reputation
        user.userprofile.save()
        return 
def granted_reputation_counter (user, reputation):
    if (reputation <0):
        if (user.userprofile.reputation + reputation < 0):
            return
        return reputation
    else:
        daily_reputation = daily_reputation_counter(user) 
        if (daily_reputation >= limit):
            return 0
        if (daily_reputation + reputation >= limit):
            return (limit - daily_reputation)
        else:
            return reputation    

def daily_reputation_counter(user):
    from datetime import datetime, date, time
    from problems.models import Problem, Solution, Rating

    today_min = datetime.combine(date.today(), time.min)
    today_max = datetime.combine(date.today(), time.max)
    try:
        daily_problems = Problem.objects.filter(user = user, added_at__range=(today_min, today_max))
        daily_solutions = Solution.objects.filter(user_id = user, added_at__range=(today_min, today_max))
        daily_ratings = Rating.objects.filter(rated_user = user, timestamp__range=(today_min, today_max))    
    except (Problem.DoesNotExist, Solution.DoesNotExist, Rating.DoesNotExist):
        pass
    daily_reputation_from_ratings = 0
    for daily_rating in daily_ratings:
        if (daily_rating.granted_reputation > 0):
            daily_reputation_from_ratings += daily_rating.granted_reputation 
    daily_reputation = 0  
    daily_reputation = daily_reputation_from_ratings + daily_problems.count()*10 + daily_solutions.count()*15   
    return daily_reputation

def within_one_hour(timestamp):
    from datetime import timedelta
    from django.utils import timezone
    now = timezone.now()
    
    
    if (now <= (timestamp + timedelta(seconds = 3600))):
        return True
    else:
        return False
    

def tag_cloud():
    from problems.models import Tag
    from django.db.models import Count
    import random
    
    tags = Tag.objects.all()
    if (tags.count()<1):
        return  
    MAX_WEIGHT = 5
    tags = Tag.objects.annotate(count = Count('problems'))
    tags = tags.annotate(weight = Count('problems'))
    
    try:
        max_count_tag = tags.latest('count')
        min_count_tag = tags.earliest('count')
    except:
        pass
    min_count = min_count_tag.count
    max_count = max_count_tag.count

    tag_range = float(max_count - min_count)
    if tag_range == 0.0:
        tag_range = 1.0
    for tag in tags:
        tag.weight = int(MAX_WEIGHT * (tag.count - min_count) / tag_range)
        
    tags = list(tags)
    random.shuffle(tags)
    return tags
    
    