from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from problems.models import  UserProfile, Ignore
from eventlog.models import Log
from django.contrib.contenttypes.models import ContentType
from problems.views.support_functions import reputation_adder


    

@login_required
def list_users(request, user_id_slug):
    context_dict = {}
    try:
        ref_user = UserProfile.objects.get(slug=user_id_slug)
        userprofile = UserProfile.objects.get(user__exact = request.user)
        context_dict['ref_user'] = ref_user
    except UserProfile.DoesNotExist:
        pass
    if request.method == 'POST':
        check = Ignore.objects.all()
        check = check.filter (user_id__exact=request.user)
        check = check.filter (ref_user_id__exact=ref_user.user)
        
        if check.exists() :
            return HttpResponse('You already ignored that user')
        else:
            
            reputation_adder(userprofile.user, -15)
            reputation_adder(ref_user, -30)
            #userprofile.reputation -= 15
            #userprofile.save()
            #ref_user.reputation -= 30
            #ref_user.save()
            new_data = Ignore(user_id = request.user, ref_user_id = ref_user.user)
            new_data.save()
            
            new_log_entry = Log(user = request.user, 
                                action = "Ignore", 
                                content_type= ContentType.objects.get_for_model(ref_user.user),
                                object_id = ref_user.pk
                                )
            new_log_entry.save()
        return HttpResponseRedirect('/problems/')
    
    else:
        return render(request, 'problems/users.html', context_dict)
