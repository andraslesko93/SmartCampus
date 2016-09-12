from django.shortcuts import render
from django.http import HttpResponseRedirect
from problems.models import Solution


def edit_solution (request, solution_id_slug):
    
    try:     
        solution = Solution.objects.get(slug=solution_id_slug)
    except Solution.DoesNotExist:
        pass
    
    if request.method == 'POST':
        served_ppl = request.POST.get("served_ppl", None)
        desc =  request.POST.get("desc", None)    
        
        solution.desc = desc
        solution.served_ppl = served_ppl
        solution.save()
        retlink = '/problems/'+ solution.problem_id.slug+'/'
        return HttpResponseRedirect(retlink)
    return render (request, 'problems/edit_solution.html', {'solution': solution})