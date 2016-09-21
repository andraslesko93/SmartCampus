from django.shortcuts import get_object_or_404, render
from problems.models import Problem

def edit_problem (request, problem_title_slug):
    problem = get_object_or_404(Problem, slug = problem_title_slug)
    render_list=({'problem': problem})
    if request.method == 'POST':
        pass
    return render (request, 'problems/edit_problem.html', render_list)