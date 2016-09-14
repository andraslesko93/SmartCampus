from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from problems.models import UserProfile, Tag, Problem, Confidence_Problem
from eventlog.models import Log
from django.contrib.contenttypes.models import ContentType
from problems.views.support_functions import reputation_adder, within_one_hour
@login_required
def add_problem(request):
    problem_limit = 5
    reputation_limit = 50
    bounty_limit = 1000
    max_bounty = 100
    confidence_problem_repu_limit = 1500  
    reached_problem_limit = True
    
    if (request.user.userprofile.reputation < reputation_limit):
            below_rep_limit = True
            return render(request, 'problems/add_problem.html', {'below_rep_limit': below_rep_limit})
    
    try:
        userprofile = UserProfile.objects.get(user__exact = request.user)
        prev_problems = Problem.objects.filter(user__exact = request.user)
        prev_problems = prev_problems.order_by('-added_at')[:problem_limit]
    except UserProfile.DoesNotExist, Problem.DoesNotExist:
        pass
    
    problems_in_one_hour = 0
    for prev_problem in prev_problems:
            if (within_one_hour(prev_problem.added_at)):
                problems_in_one_hour = problems_in_one_hour +1
        
    if (problems_in_one_hour == problem_limit):
            reached_problem_limit = True
            return render(request, 'problems/add_problem.html', {'reached_problem_limit': reached_problem_limit, 'problems_in_one_hour':problems_in_one_hour})
    
    
    render_list =({'bounty_limit': bounty_limit, 'max_bounty': max_bounty, 'confidence_problem_repu_limit': confidence_problem_repu_limit})
    
    if request.method == 'POST':
        reputation = 10   
        
        title = request.POST.get("title")
        if (title==""):
            error_message="Please enter the title of the problem"
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
        
        if (len(title)>30):
            error_message="Maximum length for the title of the problem is 30 character"
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
        
        place = request.POST.get("place")
        if (place==""):
            error_message="Please enter the place of the problem"
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
        
        if (len(place)>30):
            error_message="Maximum length for the place of the problem is 30 character"
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
        
        
        rq_ppl = request.POST.get("rq_ppl")
        if (rq_ppl==""):
            error_message  = "Please enter the ammount of the required people"
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
        
        tags = request.POST.get("tags")
        if (tags==""):
            error_message= "Please enter some tags for the problem"
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
        
        deadline = request.POST.get("deadline")
        
        desc =  request.POST.get("desc")
        if (desc==""):
            error_message="Please enter the description of the problem"
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
        
        if (len(desc)<15):
            error_message="Minimum length for Description is 15 character"
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
        if (len(desc)>300):
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
            error_message="Maximum length for Description is 300 character"
        
        rq_repu = request.POST.get("rq_repu")
        if (rq_repu==""):
            error_message="Please enter the amount of the minimum required reputation"
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
        
        bounty = request.POST.get("bounty")
        if (bounty==""):
            error_message="Please enter the amount of the bounty"
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
        
        tags = tags.lower()
        tags = tags.replace (',', ' ')
        tags = tags.replace ('  ', ' ')
        tag_list = tags.split()
        
        if (rq_repu != None):
        
            new_problem = Confidence_Problem(title = title,
                                             place = place,
                                             desc = desc,
                                             rq_ppl = rq_ppl,
                                             deadline = deadline,
                                             user = request.user, 
                                             min_rq_reputation = rq_repu
                                             )
            if (bounty != None):
                new_problem.bounty =  bounty
            new_problem.save() 
            
        else:
            new_problem = Problem(title = title,
                                  place = place,
                                  desc = desc,
                                  rq_ppl = rq_ppl,
                                  deadline = deadline,
                                  user = request.user 
                                  )
            if (bounty != None):
                new_problem.bounty =  bounty
            new_problem.save()
            
        for i in tag_list: 
            try:
                x = Tag.objects.get(tag_text=i)     
            except Tag.DoesNotExist:
                x = Tag(tag_text = i)
                x.save()
            new_problem.tags.add(x)
        new_problem.save()
        
        new_log_entry = Log(user = request.user, 
                                action = "New Problem", 
                                content_type= ContentType.objects.get_for_model(new_problem),
                                object_id = new_problem.pk,
                                extra = reputation
                                )
        new_log_entry.save()
        
        reputation_adder(userprofile.user, reputation)
        retlink = '/'
        return HttpResponseRedirect(retlink)

    return render(request, 'problems/add_problem.html', render_list)