from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from problems.models import  UserProfile, Ignore
from eventlog.models import Log
from django.contrib.contenttypes.models import ContentType
from problems.views.support_functions import reputation_adder    

@login_required
def post_user_ignore(request, user_id_slug):
    try:
        ref_user = UserProfile.objects.get(slug=user_id_slug)
        userprofile = UserProfile.objects.get(user__exact = request.user)
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
            reputation_adder(ref_user.user, -30)
            new_data = Ignore(user_id = request.user, ref_user_id = ref_user.user)
            new_data.save()
            
            new_log_entry = Log(user = request.user, 
                                action = "Ignore", 
                                content_type= ContentType.objects.get_for_model(ref_user.user),
                                object_id = ref_user.pk
                                )
            new_log_entry.save()
        return HttpResponseRedirect('/')
    
    else:
        return render(request, 'problems/users.html')
