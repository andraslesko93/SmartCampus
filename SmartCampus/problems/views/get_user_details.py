from django.contrib.auth.decorators import login_required
from problems.models import  UserProfile, Ignore
from django.http.response import HttpResponse
import json
from problems.views.user_to_json import user_to_json

@login_required
def get_user_details(request, user_id_slug):
    try:
        userprofile = UserProfile.objects.get(slug=user_id_slug)
        ignores = Ignore.objects.filter(user_id__exact=request.user)
    except UserProfile.DoesNotExist:
        return HttpResponse(json.dumps([], ensure_ascii=False).encode('utf8'))
    
    json_list=({'picture':userprofile.picture_url,
                'username':userprofile.user.username,
                'email':userprofile.user.email,
                'joined_at': userprofile.user.date_joined.strftime('%Y-%m-%d %H:%M'),
                'last_login':userprofile. user.last_login.strftime('%Y-%m-%d %H:%M'),
                'reputation':userprofile.reputation,
                'ignore':"allowed",
                })
    for ignore in ignores:
        if userprofile.user == ignore.ref_user_id: #already ignored
            json_list.update({'ignore': "forbidden"})
    if(request.user==userprofile.user): #own profile
        json_list.update({'ignore': "forbidden"})
    return HttpResponse(json.dumps(json_list, ensure_ascii=False).encode('utf8'))
    return user_to_json(request.user, userprofile.user)
