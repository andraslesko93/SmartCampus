from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from problems.models import Problem, Ignore, Tag
from django.contrib.auth.models import User
from django.db.models import Q




@login_required
def search(request):
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
    #nemertem a duplikalas miert gond, de ez megoldja
    problem_query = problem_query.distinct()
    
    users =  User.objects.filter(username__contains = hit)
    users = users.filter(~Q(pk__in=ignored_users.values('ref_user_id')))
    
    context_dict = {'hit':hit, 'problems':problem_query, 'users':users }
    return render(request, 'problems/search.html', context_dict)