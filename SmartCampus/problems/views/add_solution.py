from django.shortcuts import render
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
    render_list =({'problem':problem, 'solutions':solutions, 'user_added_solution':user_added_solution })

    if(hasattr(problem, 'confidence_problem') and request.user.userprofile.reputation < problem.confidence_problem.min_rq_reputation):
        return render(request, 'problems/problems.html', render_list)
    
    if (own_solutions.count()>0):
        user_added_solution = True
        return render(request, 'problems/problems.html', render_list)
    
    if(problem.status!="pending"):
        render_list['error_message']="You cannot add a solution to a closed problem."
        return render(request, 'problems/problems.html', render_list)
    
    if(problem.user==request.user):
        return render(request, 'problems/problems.html', render_list)
    
    if request.method == 'POST':    
        reputation = 15
        served_ppl = request.POST.get("served_ppl", None)
        desc =  request.POST.get("desc", None)
        pk_in = request.POST.get ("problems", None)
        problem = get_object_or_404(Problem, pk = pk_in)
        
        if (served_ppl==""):
            render_list['error_message']="Please add the amount of the people you serve in your solution."
            return render(request, 'problems/problems.html', render_list)
                
        if (int(served_ppl) < 1):
            render_list['error_message']="You have to serve at least one people in your solution."
            return render(request, 'problems/problems.html', render_list)
        
        if (int(served_ppl) > problem.rq_ppl):
            render_list['error_message']="You cannot serve more people than the problem requires."
            return render(request, 'problems/problems.html', render_list)
        
        if (desc==""):
            render_list['error_message']="You have to add some description to your solution."
            return render(request, 'problems/problems.html', render_list)
            pass
           
        if (len(desc)<15):
            render_list['error_message']="The description should be at least 15 character long."
            return render(request, 'problems/problems.html', render_list)
        
        if (len(desc)>500):
            render_list['error_message']="The description should be maximum 300 character long."
            return render(request, 'problems/problems.html', render_list)
        
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
    return render(request, 'problems/problems.html', render_list)
