from django.contrib.auth.decorators import login_required
from problems.models import Problem, Ignore
from django.db.models import Q
from datetime import datetime
from problems.views.problem_to_json import problem_to_json
from problems.get_disctance import get_distance

lat = None
lng = None

@login_required
def get_problems(request, deadline, problem_type):  

    lat = request.GET.get("lat", None)
    lng = request.GET.get("lng", None) 
    print lat
    print lng
    
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

    if (lat!=None and lng!=None):
        nearby_problems = []
        for problem in problems:
            distance= get_distance(float(lng), float(lat), problem.coordinates.longitude, problem.coordinates.latitude)
            if (distance <= request.user.userprofile.max_problem_distance):
                nearby_problems.append(problem)
        return problem_to_json(nearby_problems, problem_type)
    return problem_to_json(problems, problem_type)