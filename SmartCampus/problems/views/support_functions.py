from problems.models import Problem, Ignore, Solution, Rating
from datetime import datetime

def reputation_adder(user, reputation):
    
    #kell activity problem posztbol
    #kell activity solution addbol
    #kell ratingbol
    
    if (user.userprofile.reputation + reputation < 0):
        return
    
    limit = 200
    
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    
    try:
        daily_problems = Problem.objects.filter(user = user, added_at__range=(today_min, today_max))
        daily_solutions = Solution.objects.filter(user = user, added_at__range=(today_min, today_max))
        daily_ratings = Rating.objects.filter(rated_user = user, timestamp__range=(today_min, today_max))
        daily_ignores_by_user = Ignore.objects.filter(user_id = user, timestamp__range=(today_min, today_max))
        daily_ignores_by_others = Ignore.objects.filter(ref_user_id = user, timestamp__range=(today_min, today_max))

    except (Problem.DoesNotExist, Solution.DoesNotExist, Rating.DoesNotExist, Ignore.DoesNotExist):
        pass
            
        
    daily_reputation_from_ratings = 0
    
    for daily_rating in daily_ratings:
        daily_reputation_from_ratings += daily_rating.reputation
    
    daily_reputation = daily_reputation_from_ratings + daily_problems.count()*10 + daily_solutions.count()*15   
    daily_reputation = daily_reputation - (15 * daily_ignores_by_user) - (30* daily_ignores_by_others)
    
    if (daily_reputation + reputation >= limit ):
        user.userprofile.reputation += (limit - daily_reputation)
    else:
        user.userprofile.reputation += reputation
    user.userprofile.save()
    
    return