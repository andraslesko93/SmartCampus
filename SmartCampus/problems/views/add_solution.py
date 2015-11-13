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
    context_dict = {} 
    try:
        ignored_user = Ignore.objects.all()
        ignored_user = Ignore.objects.filter(ref_user_id__exact=request.user)
        problem = Problem.objects.get(slug=problem_title_slug)
        userprofile = UserProfile.objects.get(user__exact = request.user)
        
    except UserProfile.DoesNotExist, Problem.DoesNotExist:
        pass
    
    if request.method == 'POST':    
        reputation = 15
        new_data = request.POST.copy()
        new_data['status'] = 'pending'
        new_data['user'] = request.user.id
        sol_form = SolutionForm(data=new_data)
        up_form = UserProfileForm(data=new_data)
        if sol_form.is_valid():
            pk_in = request.POST.get ("add_solution", None)
            problem = get_object_or_404(Problem, pk = pk_in)            
            temp = sol_form.save(commit=False)
            temp.user_id = request.user
            temp.problem_id = problem
            
            temp.save()
            
            new_log_entry = Log(user = request.user, 
                                action = "New Solution", 
                                content_type= ContentType.objects.get_for_model(temp),
                                object_id = temp.pk,
                                extra = reputation
                                )
            new_log_entry.save()
            
            if ignored_user.count()<1:
                
                notification_entry = Notification(
                            user = problem.user,
                            content_type= ContentType.objects.get_for_model(temp),
                            object_id = temp.pk
                            )
                notification_entry.save()
        
                unchecked_notifications = Notification.objects.filter(user__exact = problem.user, status__exact = "unchecked")
                problem.user.userprofile.notification_number = unchecked_notifications.count()
                problem.user.userprofile.save()
            
            reputation_adder(userprofile.user, reputation)               
           # userprofile.reputation += reputation
           # userprofile.save()
            retlink = '/problems/add_solution/'+ problem.slug+'/'
            return HttpResponseRedirect(retlink)
        
        else:
            print sol_form.errors
    else:
        sol_form = SolutionForm()
        try:
            problem = Problem.objects.get(slug=problem_title_slug)
            context_dict['problem'] = problem
            ignored_users = Ignore.objects.all()
            ignored_users = ignored_users.filter (user_id__exact=request.user)
            solutions = Solution.objects.all()
            solutions = solutions.filter (problem_id__exact = problem)
            solutions= solutions.filter(~Q(user_id=ignored_users.values('ref_user_id')))
            context_dict['solutions'] = solutions
        except Problem.DoesNotExist:
            pass
        return render(request, 'problems/add_solution.html',{'problem':problem, 'sol_form':sol_form, 'solutions':solutions} )
