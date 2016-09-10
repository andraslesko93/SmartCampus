from django.contrib.auth.decorators import login_required
from problems.models import Notification
from django.http.response import HttpResponse
import json

@login_required
def get_notifications(request, count):
    
    if (count.isdigit()==False and count!="all"):
        return HttpResponse("Wrong parameters")
    notifications = Notification.objects.filter(user__exact = request.user)
    notifications = notifications.order_by('-timestamp')
    count_as_integer=0 
    if count.isdigit():
        count_as_integer=int(count)
    json_list = []
    for notification in notifications:
        if (notification.status == "checked" and count!="all"):
            count_as_integer = count_as_integer-1
            if count_as_integer<0:
                break
        if notification.content_type.model == "solution":
            if notification.obj.user_id == request.user:
                json_list.append({
                                  'status':notification.status,
                                  'picture':notification.obj.problem_id.user.userprofile.picture_url,
                                  'sender':notification.obj.problem_id.user.username,
                                  'problem_title': notification.obj.problem_id.title,
                                  'problem_link':"/problems/"+notification.obj.problem_id.slug,
                                  'model_type':"accepted solution",
                                  })
            else:
                json_list.append({
                                  'status':notification.status,
                                  'picture':notification.obj.user_id.userprofile.picture_url,
                                  'sender':notification.obj.user_id.username,
                                  'problem_title':notification.obj.problem_id.title,
                                  'problem_link':"/problems/"+notification.obj.problem_id.slug,
                                  'model_type':"offered solution",
                                  })
            
        if notification.content_type.model == "rating":
            json_list.append({
                              'status':notification.status,
                              'picture':notification.obj.user.userprofile.picture_url,
                              'sender':notification.obj.user.username,
                              'problem_title':notification.obj.solution.problem_id.title,
                              'problem_link':"/problems/"+notification.obj.solution.problem_id.slug,
                              'model_type': notification.obj.type,
                              'bounty':notification.obj.bounty,
                              'granted_reputation':notification.obj.granted_reputation,
                              'reputation':notification.obj.reputation,
                              })
        if notification.content_type.model == "user":
            json_list.append({
                              'status':notification.status,
                              'picture':"/media/profile_images/SC_logo.png",
                              'sender':"SmartCampus",
                              'problem_link':"/about/",
                              'model_type': "user",
                              'granted_reputation':100,
                              'reputation':100,
                              })
    return HttpResponse(json.dumps(json_list, ensure_ascii=False).encode('utf8'))