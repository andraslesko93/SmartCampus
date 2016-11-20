from django.http.response import HttpResponse
import json
from django.utils.html import escape

def problem_to_json(problems, problem_type):
    json_list = []
    for problem in problems:
        tag_list = []
        for tag in problem.tags.all():
            tag_list.append({'tag_text':tag.tag_text, 'tag_link':"/tag/"+tag.slug})
        if (problem_type == "classic"):
            json_list.append({
                          'user': problem.user.username,
                          'picture':problem.user.userprofile.picture_url,
                          'user_link':"/users/"+problem.user.userprofile.slug,
                          'title': problem.title,
                          'problem_link':"/problems/"+problem.slug,
                          'place': problem.place,
                          'description': escape(problem.desc),
                          'deadline': problem.deadline.strftime('%Y-%m-%d %H:%M'),
                          'tags':tag_list,
                          'bounty': problem.bounty
            })     
        elif (problem_type == "confidence"):
            json_list.append({
                          'user': problem.user.username,
                          'picture':problem.user.userprofile.picture_url,
                          'user_link':"/users/"+problem.user.userprofile.slug,
                          'title': problem.title,
                          'problem_link':"/problems/"+problem.slug,
                          'place': problem.place,
                          'description': problem.desc,
                          'deadline': problem.deadline.strftime('%Y-%m-%d %H:%M'),
                          'tags':tag_list,
                          'bounty': problem.bounty,
                          'minimum_required_reputation': problem.confidence_problem.min_rq_reputation
            })
        elif (problem_type == "mixed"):
            if(problem.__class__.__name__ =="Problem"):
                json_list.append({
                          'user': problem.user.username,
                          'picture':problem.user.userprofile.picture_url,
                          'user_link':"/users/"+problem.user.userprofile.slug,
                          'title': problem.title,
                          'problem_link':"/problems/"+problem.slug,
                          'description': problem.desc,
                          'deadline': problem.deadline.strftime('%Y-%m-%d %H:%M'),
                          'tags':tag_list,
                          'bounty': problem.bounty,
            })
            else:
                json_list.append({
                          'user': problem.user.username,
                          'picture':problem.user.userprofile.picture_url,
                          'user_link':"/user/"+problem.user.userprofile.slug,
                          'title': problem.title,
                          'problem_link':"/problems/"+problem.slug,
                          'description': problem.desc,
                          'deadline': problem.deadline.strftime('%Y-%m-%d %H:%M'),
                          'tags':tag_list,
                          'bounty': problem.bounty,
                          'minimum_required_reputation': problem.confidence_problem.min_rq_reputation
            })      
            
    for json_list_element in json_list:
        escape(json_list_element)
    return HttpResponse(json.dumps(json_list, ensure_ascii=False).encode('utf8'))             