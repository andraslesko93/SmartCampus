from django.shortcuts import render
from problems.forms import UserProfileForm, SolutionForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from problems.models import Problem, Solution, UserProfile, Ignore, Notification
from django.shortcuts import get_object_or_404
from django.db.models import Q
from eventlog.models import Log
from django.contrib.contenttypes.models import ContentType
from problems.views.support_functions import reputation_adder

@login_required
def add_solution(request, problem_title_slug):
    try:
        ignored_users = Ignore.objects.all()
        ignored_users = Ignore.objects.filter(ref_user_id__exact=request.user)
        problem = Problem.objects.get(slug=problem_title_slug)
        userprofile = UserProfile.objects.get(user__exact = request.user)
        solutions = Solution.objects.filter (problem_id__exact = problem)
        solutions = solutions.filter( ~Q(user_id=ignored_users.values('ref_user_id')))        
        own_solutions = Solution.objects.filter(problem_id__exact = problem, user_id__exact= request.user)
    except (UserProfile.DoesNotExist, Problem.DoesNotExist, Ignore.DoesNotExist, Solution.DoesNotExist):
        pass
    
    user_added_solution = False
    if (own_solutions.count()>0):
        user_added_solution = True
        return render(request, 'problems/problems.html',{'problem':problem, 'solutions':solutions, 'user_added_solution':user_added_solution } )

    if request.method == 'POST':    
        reputation = 15
        served_ppl = request.POST.get("served_ppl", None)
        desc =  request.POST.get("desc", None)
        pk_in = request.POST.get ("problems", None)
        problem = get_object_or_404(Problem, pk = pk_in)
        
        new_solution = Solution(user_id = request.user,
                                served_ppl = served_ppl,
                                desc = desc,
                                problem_id = problem
                                )
        new_solution.save()
        new_log_entry = Log(user = request.user, 
                                action = "New Solution", 
                                content_type= ContentType.objects.get_for_model(new_solution),
                                object_id = new_solution.pk,
                                extra = reputation
                                )
        new_log_entry.save()
        if ignored_users.count()<1:
            
            notification_entry = Notification(
                        user = problem.user,
                        content_type= ContentType.objects.get_for_model(new_solution),
                        object_id = new_solution.pk
                        )
            notification_entry.save()     
        reputation_adder(userprofile.user, reputation)  
        retlink = '/problems/'+ problem.slug+'/'
        return HttpResponseRedirect(retlink)
    return render(request, 'problems/problems.html',{'problem':problem, 'user_added_solution': user_added_solution, 'solutions':solutions} )
