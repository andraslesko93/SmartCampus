from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from problems.models import Ignore
from django.shortcuts import get_object_or_404
from eventlog.models import Log
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt


@login_required
def post_user_unblock(request):
    if request.method == 'POST' and request.is_ajax():
        user_id = request.POST.get ("id", None)
        user_id=int(user_id)
        ignore = Ignore.objects.filter(ref_user_id__exact=user_id)        
        ignore.delete()

    return render(request, 'problems/ignored_users.html')  