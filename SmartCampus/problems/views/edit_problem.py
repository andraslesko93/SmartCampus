from django.shortcuts import get_object_or_404, render
from problems.models import Problem, Tag
from eventlog.models import Log
from problems.views.reputation_system_settings import bounty_limit
import datetime
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect


def edit_problem (request, problem_title_slug):    
    problem = get_object_or_404(Problem, slug = problem_title_slug)
    
    if(problem.user!=request.user):
        error_message="You can not edit other's problems."
        return render(request, 'problems/edit_problem.html', {'error_message':error_message})
    
    if(problem.status!="new"):
        error_message="You can not edit a pending problem."
        return render(request, 'problems/edit_problem.html', {'error_message':error_message})
 
    tags=""
    for tag in problem.tags.all():
        tags += tag.tag_text 
    deadline = str(problem.deadline)    
    deadline=deadline.replace(" ", "T")
    
    is_confidence = False
    if (hasattr(problem, 'confidence_problem')):
        is_confidence =True
    
    render_list=({'problem': problem, 'bounty_limit':bounty_limit, 'tags': tags, 'deadline':deadline, 'is_confidence':is_confidence})
    
    if request.method == 'POST':
        title = request.POST.get("title")
        if (title==""):
            error_message="Please enter the title of the problem."
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
        
        if (len(title)>30):
            error_message="Maximum length for the title of the problem is 30 character."
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
        
        place = request.POST.get("place")
        if (place==""):
            error_message="Please enter the place of the problem."
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
        
        if (len(place)>30):
            error_message="Maximum length for the place of the problem is 30 character."
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
        
        
        rq_ppl = request.POST.get("rq_ppl")
        if (rq_ppl==""):
            error_message  = "Please enter the amount of the required people."
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
        
        tags = request.POST.get("tags")
        if (tags==""):
            error_message= "Please enter some tags for the problem."
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
        
        deadline = request.POST.get("deadline")
        if (deadline==""):
            error_message="Please enter the deadline of the problem."
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
                
        date_in = deadline 
        date_out = datetime.datetime(*[int(v) for v in date_in.replace('T', '-').replace(':', '-').split('-')])
        
        if(date_out<(datetime.datetime.now())):
            error_message="You can't edit a problem's deadline to the past."
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
        
        if(date_out<(datetime.datetime.now() + datetime.timedelta(days=0, hours=1))):
            error_message="You can't edit a problem's deadline to such a close deadline. There should be at least 1 hour until its deadline passes." +str(deadline)
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
        desc =  request.POST.get("desc")
        if (desc==""):
            error_message="Please enter the description of the problem."
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
        
        if (len(desc)<15):
            error_message="Minimum length for Description is 15 character"
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
        if (len(desc)>500):
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
            error_message="Maximum length for Description is 300 character."
        
        rq_repu = request.POST.get("rq_repu")
        if (rq_repu=="" and is_confidence):
            error_message="Please enter the amount of the minimum required reputation."
            render_list['error_message']=error_message
            return render(request, 'problems/add_problem.html', render_list)
        
        bounty = request.POST.get("bounty")
        tags = tags.lower()
        tags = tags.replace (',', ' ')
        tags = tags.replace ('  ', ' ')
        tag_list = tags.split()
        
        if (rq_repu != None):
            problem.title = title
            problem.place = place
            problem.desc = desc
            problem.rq_ppl = rq_ppl
            problem.deadline = deadline
            problem.min_rq_reputation = rq_repu
            if (bounty != None):
                problem.bounty =  bounty            
        else:
            problem.title = title
            problem.place = place
            problem.desc = desc
            problem.rq_ppl = rq_ppl
            problem.deadline = deadline
            if (bounty != None):
                problem.bounty =  bounty
            
        for i in tag_list: 
            try:
                x = Tag.objects.get(tag_text=i)     
            except Tag.DoesNotExist:
                x = Tag(tag_text = i)
                x.save()
            problem.tags.add(x)
        problem.save()
        new_log_entry = Log(user = request.user, 
                                action = "Edit a problem", 
                                content_type= ContentType.objects.get_for_model(problem),
                                object_id = problem.pk,
                                )
        new_log_entry.save()
        retlink = '/own_problems/'
        return HttpResponseRedirect(retlink)
    return render (request, 'problems/edit_problem.html', render_list)