from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from problems.models import Ignore
from django.shortcuts import get_object_or_404
from eventlog.models import Log
from django.contrib.contenttypes.models import ContentType



@login_required
def ignored_users(request):
    ignored_users = Ignore.objects.all()
    ignored_users = ignored_users.filter (user_id__exact=request.user)
    context_dict = {'ignored_users': ignored_users}
    if request.method == 'POST':
        pk_in = request.POST.get ("user_rem_ignore_list", None)
        ignored_user = get_object_or_404(Ignore, pk = pk_in)
        
        new_log_entry = Log(user = request.user, 
                                action = "Remove Ignore", 
                                content_type= ContentType.objects.get_for_model(ignored_user.ref_user_id),
                                object_id = ignored_user.ref_user_id.pk
                                )
        new_log_entry.save()
        
        ignored_user.delete()
        
        
        
    return render(request, 'problems/ignored_users.html', context_dict)  