from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from problems.models import Solution, Rating, Notification
from eventlog.models import Log
from django.contrib.contenttypes.models import ContentType
    

@login_required
def accept_solution(request, solution_id_slug):
    context_dict = {}
    try:
        
        solution = Solution.objects.get(slug=solution_id_slug)
        problem = solution.problem_id
        context_dict['solution'] = solution
        
    except Solution.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass
    
    if request.method == 'POST' and request.user == problem.user:   
        solution.status = 'accepted'
        solution.save()
        problem.rq_ppl = problem.rq_ppl - solution.served_ppl
        problem.save()
        if (problem.rq_ppl <= 0):
            try:
                accepted_solutions = Solution.objects.filter(problem_id__exact = problem)
                accepted_solutions = accepted_solutions.filter(status__exact = 'accepted')
                total_served_ppl = 0
                for accepted_solution in accepted_solutions:
                    total_served_ppl += accepted_solution.served_ppl
                
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
                                bounty = accepted_solution.served_ppl * (problem.bounty/total_served_ppl),
                                type = "rate solution author"             
                                )
                    rate_solution_author_entry.save()
                    
                request.user.userprofile.reputation -= problem.bounty
                request.user.userprofile.save()
            except Solution.DoesNotExist:
                pass
            problem.status = 'in_progress'
            problem.save()

        
        notification_entry = Notification(
                            user = solution.user_id,
                            content_type= ContentType.objects.get_for_model(solution),
                            object_id = solution.pk
                            )
        notification_entry.save()
        
        new_log_entry = Log(user = request.user, 
                                action = "Accept a solution", 
                                content_type= ContentType.objects.get_for_model(solution),
                                object_id = solution.pk
                                )
        new_log_entry.save()
        
        
        
        retlink = '/problems/'+ problem.slug+'/'
        return HttpResponseRedirect(retlink)
    return render(request, 'problems/accept_solution.html', context_dict)
