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
        problem_list = problem_list.filter (status__exact="pending")
        problem_list = problem_list.filter (deadline__lte=datetime.now())
        problem_list = problem_list.filter(~Q(user=ignored_users.values('ref_user_id')))
        context_dict = {'outdated_problems': problem_list}

    # Render the response and send it back!
    return render(request, 'problems/outdated.html', context_dict)