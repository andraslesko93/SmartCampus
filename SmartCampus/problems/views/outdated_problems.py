from django.shortcuts import render
from datetime import datetime
from problems.models import Problem, Ignore
from django.db.models import Q


def outdated(request):
    context_dict = {}
    if  request.user.is_authenticated(): 
        ignored_users = Ignore.objects.all()
        ignored_users = ignored_users.filter (user_id__exact=request.user)
        problem_list = Problem.objects.all()
        problem_list = Problem.objects.order_by('-deadline')
        problem_list = problem_list.filter (Q(status__exact = "pending") | Q(status__exact = "new")) 
        problem_list = problem_list.filter (deadline__lte=datetime.now())
        problem_list = problem_list.filter(~Q(user=ignored_users.values('ref_user_id')))
        classic_problem_list = problem_list.filter(confidence_problem__isnull = True)
        confidence_problem_list = problem_list.filter(confidence_problem__isnull = False)
        

        context_dict = {'classic_problems': classic_problem_list, 'confidence_problems' : confidence_problem_list}

    # Render the response and send it back!
    return render(request, 'problems/outdated.html', context_dict)