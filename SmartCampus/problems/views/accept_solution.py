from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from problems.models import Solution, UserProfile, Rating, Notification
from eventlog.models import Log
from django.contrib.contenttypes.models import ContentType


    

@login_required
def accept_solution(request, solution_id_slug):
    context_dict = {}
    try:
        
        solution = Solution.objects.get(slug=solution_id_slug)
        context_dict['solution'] = solution
        
    except Solution.DoesNotExist, UserProfile.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass
    
    if request.method == 'POST' and request.user == solution.problem_id.user:   
        solution.status = 'accepted'
        solution.save()
        solution.problem_id.rq_ppl = solution.problem_id.rq_ppl - solution.served_ppl
        solution.problem_id.save()
        if (solution.problem_id.rq_ppl <= 0):
            try:
                accepted_solutions = Solution.objects.filter(problem_id__exact = solution.problem_id)
                accepted_solutions = accepted_solutions.filter(status__exact = 'accepted')
                for accepted_solution in accepted_solutions:
                    
                    rate_problem_author_entry = Rating(
                                user = accepted_solution.user_id,
                                rated_user = request.user,
                                solution = accepted_solution,
                                type = "rate problem author"         
                                )
                    rate_problem_author_entry.save()
                    
                    
                    rate_solution_author_entry = Rating(
                                user = request.user,
                                rated_user = accepted_solution.user_id,
                                solution = accepted_solution,
                                type = "rate solution author"             
                                )
                    rate_solution_author_entry.save()
                    
                    solution_giver_ratings = Rating.objects.filter (user__exact= accepted_solution.user_id, status__exact ="pending") 
                    accepted_solution.user_id.userprofile.rating_number = solution_giver_ratings.count()
                    accepted_solution.user_id.userprofile.save()
                
                solution_accepter_rating = Rating.objects.filter (user__exact = request.user, status__exact ="pending")
                request.user.userprofile.rating_number = solution_accepter_rating.count()
                request.user.userprofile.save()
                    
                    
            except Solution.DoesNotExist:
                pass
            solution.problem_id.status = 'accepted'
            solution.problem_id.save()

        
        notification_entry = Notification(
                            user = solution.user_id,
                            content_type= ContentType.objects.get_for_model(solution),
                            object_id = solution.pk
                            )
        notification_entry.save()
        
        unchecked_notifications = Notification.objects.filter(user__exact = solution.user_id, status__exact = "unchecked")
        solution.user_id.userprofile.notification_number = unchecked_notifications.count()
        solution.user_id.userprofile.save() 
        
        new_log_entry = Log(user = request.user, 
                                action = "Accept a solution", 
                                content_type= ContentType.objects.get_for_model(solution),
                                object_id = solution.pk
                                )
        new_log_entry.save()
        
        
        
        retlink = '/problems/add_solution/'+ solution.problem_id.slug+'/'
        return HttpResponseRedirect(retlink)
    return render(request, 'problems/accept_solution.html', context_dict)
