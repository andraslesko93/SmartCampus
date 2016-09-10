from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from problems.models import Rating, Notification
from django.shortcuts import get_object_or_404
from eventlog.models import Log
from django.contrib.contenttypes.models import ContentType
from problems.views.support_functions import reputation_adder, granted_reputation_counter
from datetime import datetime


@login_required
def post_ratings(request):
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
                    solution_author.userprofile.reputation += rating.bounty
                    solution_author.userprofile.save()
                else:
                    reputation = (multiplier /2) * (behaviour+helpful+further_help +1)
                    reputation = reputation *-1
                    rating.user.userprofile.reputation += rating.bounty
                    rating.bounty = 0
                    rating.user.userprofile.save()
                    #solution_author.userprofile.reputation -= reputation
            else:
                if (appeared_people > 0):
                    reputation = appeared_people*multiplier*(behaviour+helpful+further_help +1)
                    
                    gained_bounty = (float(appeared_people) / (rating.solution.served_ppl)) * rating.bounty
                    solution_author.userprofile.reputation += gained_bounty
                   
                    solution_author.userprofile.save()
                    
                    if (rating.bounty-gained_bounty > 0):
                        rating.user.userprofile.reputation += int(rating.bounty-gained_bounty)
                        rating.user.userprofile.save()
                    #solution_author.userprofile.reputation += reputation  
                    rating.bounty = gained_bounty
                else:
                    reputation = (multiplier /2) * (behaviour+helpful+further_help +1)
                    reputation = reputation *-1
                    rating.user.userprofile.reputation += rating.bounty
                    rating.bounty = 0
                    rating.user.userprofile.save()
            
            reputation_adder(solution_author, reputation)
            rating.reputation = reputation
            rating.timestamp = datetime.now()
            rating.granted_reputation = granted_reputation_counter(solution_author, reputation)
            rating.status = "complete"
            rating.save()
            
            notification_entry = Notification(
                            user = solution_author,
                            content_type= ContentType.objects.get_for_model(rating),
                            object_id = rating.pk
                            )
            notification_entry.save()            
            
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
            rating.timestamp = datetime.now()
            rating.granted_reputation = granted_reputation_counter(problem_author, reputation)
            rating.status = "complete"
            rating.save()
            rating.solution.problem_id.status = "solved"
            rating.solution.problem_id.save()
            
            notification_entry = Notification(
                            user = problem_author,
                            content_type= ContentType.objects.get_for_model(rating),
                            object_id = rating.pk
                            )
            notification_entry.save()
            
            new_log_entry = Log(user = request.user, 
                                action = "New Rating", 
                                extra =  reputation,
                                content_type= ContentType.objects.get_for_model(rating),
                                object_id = rating.pk
                                )
            new_log_entry.save()
    context_dict = {'rate_solution_authors':rate_solution_authors, 'rate_problem_authors' : rate_problem_authors}
    return render(request, 'problems/ratings.html', context_dict)


