from django.contrib.auth.decorators import login_required
from problems.models import Ignore, UserProfile
from django.contrib.auth.models import User
from django.db.models import Q
from problems.views.user_to_json import user_to_json
from django.http.response import HttpResponse
import json
@login_required
def get_users_by_keyword(request):
    if request.method == 'GET':
        hit = request.GET.get('query', '')
    ignored_users = Ignore.objects.filter (user_id__exact=request.user)
    users =  User.objects.filter(username__contains = hit)
    users = users.filter(~Q(pk__in=ignored_users.values('ref_user_id')))
    
    json_list = []
    for user in users:
        json_list.append({'picture':user.userprofile.picture_url,
                          'user_link':"/users/"+user.userprofile.slug,
                          'user_name':user.username,
                          'reputation':user.userprofile.reputation
                          })
    return HttpResponse(json.dumps(json_list, ensure_ascii=False).encode('utf8'))         
    
        