from django.contrib.auth.decorators import login_required
from problems.models import Problem, Ignore
from django.db.models import Q
from datetime import datetime
from problems.views.problem_to_json import problem_to_json

@login_required
def get_problems(request, deadline, problem_type):  
    ignored_users = Ignore.objects.filter (user_id__exact=request.user)
    problems= Problem.objects.all()        
    problems = problems.order_by('-bounty', 'deadline')
    problems = problems.filter (Q(status__exact = "pending") | Q(status__exact = "new"))   
    problems = problems.filter(~Q(user=ignored_users.values('ref_user_id')))    
    if (deadline == "in_time"):
        problems = problems.filter(deadline__gte=datetime.now())
    elif (deadline == "outdated"):
        problems = problems.filter (deadline__lte=datetime.now())    
    if (problem_type == "classic"):
        problems = problems.filter(confidence_problem__isnull = True)
    elif (problem_type=="confidence"):
        problems = problems.filter(confidence_problem__isnull = False)
    
    return problem_to_json(problems, problem_type)