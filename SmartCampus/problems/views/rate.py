from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from problems.models import Rating, Notification
from django.shortcuts import get_object_or_404
from eventlog.models import Log
from django.contrib.contenttypes.models import ContentType
from problems.views.support_functions import reputation_adder



@login_required
def rate(request):
    try:      
        rate_solution_authors= Rating.objects.filter(user__exact = request.user, status__exact = "pending", type__exact= "rate solution author")   
        rate_problem_authors = Rating.objects.filter(user__exact = request.user, status__exact = "pending", type__exact = "rate problem author")         
    except Rating.DoesNotExist:
        pass
    if request.method == 'POST':
        rate_solution_author = request.POST.get("rate_solution_author", None)
        rate_problem_author = request.POST.get('rate_problem_author', None)
        appeared = request.POST.get("appeared", None)
        appeared_people = request.POST.get("appeared_people", None)
        behaviour = request.POST.get("behaviour", None)
        
        behaviour = int(behaviour)
        helpful = request.POST.get("helpful", None)
        helpful = int(helpful)
        further_help = request.POST.get("further_help", None)
        further_help = int(further_help)
        if (appeared_people != None):
            appeared_people = int(appeared_people)
        reputation = 0
        
        if (rate_solution_author):
            multiplier = 10
            rating = get_object_or_404(Rating, pk = rate_solution_author)
            solution_author = rating.rated_user
            if (rating.solution.served_ppl == 1):
                if (appeared == "yes" ):
                    reputation = multiplier*(behaviour+helpful+further_help +1)
                    #solution_author.userprofile.reputation += reputation
                else:
                    reputation = (multiplier /2) * (behaviour+helpful+further_help +1)
                    reputation = reputation *-1
                    #solution_author.userprofile.reputation -= reputation
            else:
                if (appeared_people > 0):
                    reputation = appeared_people*multiplier*(behaviour+helpful+further_help +1)
                    #solution_author.userprofile.reputation += reputation  
                else:
                    reputation = (multiplier /2) * (behaviour+helpful+further_help +1)
                    reputation = reputation *-1
                    #solution_author.userprofile.reputation -= reputation
            
            reputation_adder(solution_author, reputation)
            rating.reputation = reputation
            rating.status = "complete"
            rating.save()
            
            notification_entry = Notification(
                            user = solution_author,
                            content_type= ContentType.objects.get_for_model(rating),
                            object_id = rating.pk
                            )
            notification_entry.save()       
                
            unchecked_notifications = Notification.objects.filter(user__exact = solution_author, status__exact = "unchecked")
            solution_author.userprofile.notification_number = unchecked_notifications.count()
            solution_author.userprofile.save()         
            
            new_log_entry = Log(user = request.user, 
                                action = "New Rating", 
                                extra =  reputation,
                                content_type= ContentType.objects.get_for_model(rating),
                                object_id = rating.pk
                                )
            new_log_entry.save()
            
            
            
        if (rate_problem_author):
            multiplier = 5
            rating = get_object_or_404(Rating, pk = rate_problem_author)
            problem_author = rating.rated_user
            if (appeared == "yes"):
                reputation = multiplier*(behaviour+helpful+further_help +1)
                #problem_author.userprofile.reputation += reputation
            else:
                reputation = (multiplier /2) * (behaviour+helpful+further_help +1)
                reputation = reputation *-1
                #problem_author.userprofile.reputation -= reputation
            
            reputation_adder(problem_author, reputation)
            rating.reputation = reputation
            rating.status = "complete"
            rating.save()
            
            notification_entry = Notification(
                            user = problem_author,
                            content_type= ContentType.objects.get_for_model(rating),
                            object_id = rating.pk
                            )
            notification_entry.save()       
                
            unchecked_notifications = Notification.objects.filter(user__exact = problem_author, status__exact = "unchecked")
            problem_author.userprofile.notification_number = unchecked_notifications.count()
            problem_author.userprofile.save()
            
            new_log_entry = Log(user = request.user, 
                                action = "New Rating", 
                                extra =  reputation,
                                content_type= ContentType.objects.get_for_model(rating),
                                object_id = rating.pk
                                )
            new_log_entry.save()
            
    try:
        pending_ratings = Rating.objects.filter(user__exact = request.user, status__exact = "pending")
        request.user.userprofile.rating_number = pending_ratings.count()
        request.user.userprofile.save()
    except Rating.DoesNotExist:
        pass
    context_dict = {'rate_solution_authors':rate_solution_authors, 'rate_problem_authors' : rate_problem_authors}
    return render(request, 'problems/rate.html', context_dict)


