from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from problems.models import Problem, Ignore, Tag
from django.contrib.auth.models import User
from django.db.models import Q
from problems.views.problem_to_json import problem_to_json

@login_required
def get_problems_by_keyword(request):
    if request.method == 'GET':
        hit = request.GET.get('query', '')
    ignored_users = Ignore.objects.filter (user_id__exact=request.user)
    problem_title_query = Problem.objects.filter(title__contains = hit, status__exact = "pending", deadline__gte=datetime.now())
    problem_title_query = problem_title_query.filter(~Q(user=ignored_users.values('ref_user_id')))
    
    problem_desc_query = Problem.objects.filter(desc__contains = hit,  status__exact = "pending", deadline__gte=datetime.now())
    problem_desc_query = problem_desc_query.filter(~Q(user=ignored_users.values('ref_user_id')))
    
    tag = Tag.objects.filter (tag_text__contains = hit)
    problem_tag_query = Problem.objects.filter(tags = tag,  status__exact = "pending", deadline__gte=datetime.now())
    problem_tag_query = problem_tag_query.filter(~Q(user=ignored_users.values('ref_user_id')))
    problem_query = problem_title_query | problem_desc_query | problem_tag_query
    problem_query = problem_query.distinct()
    problem_query = problem_query.order_by('-bounty', 'deadline') 
    return problem_to_json(problem_query, "mixed")
