from django.shortcuts import render#, render_to_response
from django.contrib.auth.decorators import login_required
from problems.models import Problem


@login_required
def own_problems(request):
    problem_list = Problem.objects.order_by('-deadline')
    problem_list = problem_list.filter (user__exact=request.user)
    
    pending_problems = problem_list.filter (status__exact = "pending")
    in_progress_problems = problem_list.filter (status__exact = "in_progress")
    solved_problems = problem_list.filter (status__exact = "solved")
    context_dict = {'pending_problems': pending_problems, 'in_progress_problems': in_progress_problems, 'solved_problems': solved_problems}
    return render(request, 'problems/own_problems.html', context_dict)
