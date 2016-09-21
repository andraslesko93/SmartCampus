from django.contrib.auth.decorators import login_required
from problems.models import Problem, Tag
from problems.views.problem_to_json import problem_to_json

@login_required
def get_problems_by_tag(request, tag_id_slug, problem_type):
    try:
        problems = Problem.objects.all()
        tag = Tag.objects.all()
        tag = tag.filter (slug = tag_id_slug)
        problems = problems.filter(tags = tag)
        problems = problems.order_by('-bounty', 'deadline')
        #does not need a deadline filter
        if (problem_type == "classic"):
            problems = problems.filter(confidence_problem__isnull = True)
        elif (problem_type=="confidence"):
            problems = problems.filter(confidence_problem__isnull = False)
    except Problem.DoesNotExist:
        pass    
    return problem_to_json(problems, problem_type)