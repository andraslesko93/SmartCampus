from django.shortcuts import render
from datetime import datetime
from problems.models import Problem, Ignore
from django.db.models import Q

from support_functions import reputation_adder

def index(request):
    context_dict = {}
    if  request.user.is_authenticated(): 
        
        #reputation_adder(request.user, 30)
        
        ignored_users = Ignore.objects.all()
        ignored_users = ignored_users.filter (user_id__exact=request.user)
        problem_list = Problem.objects.all()
        problem_list = Problem.objects.order_by('deadline')
        problem_list = problem_list.filter (status__exact="pending")
        problem_list = problem_list.filter (deadline__gte=datetime.now())
        problem_list = problem_list.filter(~Q(user=ignored_users.values('ref_user_id')))    
        context_dict = {'problems': problem_list}       
    return render(request, 'problems/index.html', context_dict)