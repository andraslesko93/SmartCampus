from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
def post_problem_disctance(request):
    
    if request.method=="POST":
        max_problem_disctance=request.POST.get("maxProblemDisctance")
        request.user.userprofile.max_problem_distance=max_problem_disctance
        request.user.userprofile.save()
        return HttpResponse("ok")
    return HttpResponse(status=204)