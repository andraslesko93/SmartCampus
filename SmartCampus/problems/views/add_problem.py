from django.shortcuts import render
from problems.forms import ProblemForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from problems.models import UserProfile, Tag
from eventlog.models import Log
from django.contrib.contenttypes.models import ContentType
from problems.views.support_functions import reputation_adder


@login_required
def add_problems(request):
    try:
        userprofile = UserProfile.objects.get(user__exact = request.user)
        
    except UserProfile.DoesNotExist:
        pass
    if request.method == 'POST': 
        if (request.user.userprofile.reputation < 50):
            return HttpResponse('You cannot create a problem with low reputation. You should help others first')
        else:
            reputation = 10   
            new_data = request.POST.copy()
            new_data['status'] = 'pending'
            new_data['added_at'] = datetime.now()
            new_data['user'] = request.user.id
            
            tags = request.POST.get("tags")
            tags = tags.lower()
            tags = tags.replace (',', ' ')
            tags = tags.replace ('  ', ' ')
            tag_list = tags.split()
            form = ProblemForm(data=new_data)
            if form.is_valid():
                temp = form.save(commit=False)
                temp.key_field = request.user
                temp.save()
                for i in tag_list: 
                    try:
                        x = Tag.objects.get(tag_text=i)     
                    except Tag.DoesNotExist:
                        x = Tag(tag_text = i)
                        x.save()
                    temp.tags.add(x)
                temp.save()
                
                new_log_entry = Log(user = request.user, 
                                    action = "New Problem", 
                                    content_type= ContentType.objects.get_for_model(temp),
                                    object_id = temp.pk,
                                    extra = reputation
                                    )
                new_log_entry.save()
                
                reputation_adder(userprofile.user, reputation)
                #userprofile.reputation += reputation
                #userprofile.save()
                retlink = '/problems/'
                return HttpResponseRedirect(retlink)
            else:
                print form.errors
                return HttpResponse('Invalid or missing parameters')
    else:
        form = ProblemForm()
        return render(request, 'problems/add_problem.html', {'form': form})