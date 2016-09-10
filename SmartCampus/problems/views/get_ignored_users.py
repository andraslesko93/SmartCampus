from problems.models import Ignore
from django.http.response import HttpResponse
import json

def get_ignored_users(request):
    ignores = Ignore.objects.filter(user_id__exact=request.user)
    json_list = []
    for ignore in ignores:
        json_list.append({
                          'username':ignore.ref_user_id.username,
                          'id': ignore.ref_user_id.id
                          })
        
    return HttpResponse(json.dumps(json_list, ensure_ascii=False).encode('utf8'))
        