from django.http.response import HttpResponse
import json

def user_to_json(curr_user, user):
    if(user==[]):
        return HttpResponse(json.dumps(user, ensure_ascii=False).encode('utf8'))
    json_list=({'picture':user.userprofile.picture_url,
                'username':user.username,
                'email':user.email,
                'joined_at': user.date_joined.strftime('%Y-%m-%d %H:%M'),
                'last_login': user.last_login.strftime('%Y-%m-%d %H:%M'),
                'reputation':user.userprofile.reputation,
                })
    if(user==curr_user):
        json_list.update({'ignore': "forbidden"})
    return HttpResponse(json.dumps(json_list, ensure_ascii=False).encode('utf8'))