from problems.models import Rating
from django.http.response import HttpResponse
import json
def get_ratings(request, requested_type):
    try:
        ratings = Rating.objects.filter(user__exact = request.user, status__exact = "pending")
    except Rating.DoesNotExist:
        pass
    if(requested_type == "rate_solution_author"):
        ratings= ratings.filter(type__exact= "rate solution author")   
    elif(requested_type =="rate_problem_author"):
        ratings=ratings.filter(type__exact = "rate problem author")
    json_list = []
    for rating in ratings:
        json_list.append({
                          'user_link': "/users/"+rating.rated_user.userprofile.slug,
                          'picture': rating.rated_user.userprofile.picture_url,
                          'username': rating.rated_user.username,
                          'rating_id': rating.pk,
                          'problem_title': rating.solution.problem_id.title,
                          'problem_link':"/problems/"+ rating.solution.problem_id.slug,
                          'served people': rating.solution.served_ppl,
                          'solution_description': rating.solution.desc,
                          })

    
    return HttpResponse(json.dumps(json_list, ensure_ascii=False).encode('utf8'))