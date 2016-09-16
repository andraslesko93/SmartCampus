from django.shortcuts import render
from django.http import HttpResponseRedirect
from problems.models import Solution
from django.shortcuts import get_object_or_404

def edit_solution (request, solution_id_slug):
    
    solution = get_object_or_404(Solution, slug = solution_id_slug)
    
    if(solution.user_id!=request.user):
        error_message="You can not edit other's solutions."
        return render(request, 'problems/edit_solution.html', {'error_message':error_message})
    
    if(solution.status!="pending"):
        error_message="You can not edit an accepted problem"
        return render(request, 'problems/edit_solution.html', {'error_message':error_message})
    render_list=({'solution': solution})
    if request.method == 'POST':
        served_ppl = request.POST.get("served_ppl", None)
        desc =  request.POST.get("desc", None)    
        
        if (served_ppl==""):
            render_list['error_message']="Please add the amount of the people you serve in your solution"
            return render(request, 'problems/edit_solution.html', render_list)
                
        if (int(served_ppl) < 1):
            render_list['error_message']="You have to serve at least one people in your solution"
            return render(request, 'problems/edit_solution.html', render_list)
        
        #if (int(served_ppl) > problem.rq_ppl):
         #   render_list['error_message']="You cannot serve more people than the problem requires"
          #  return render(request, 'problems/problems.html', render_list)
        
        if (desc==""):
            render_list['error_message']="You have to add some description to your solution"
            return render(request, 'problems/edit_solution.html', render_list)
            pass
           
        if (len(desc)<15):
            render_list['error_message']="The description should be at least 15 character long"
            return render(request, 'problems/edit_solution.html', render_list)
        
        if (len(desc)>500):
            render_list['error_message']="The description should be maximum 300 character long"
            return render(request, 'problems/edit_solution.html', render_list)
        
        solution.desc = desc
        solution.served_ppl = served_ppl
        solution.save()
        retlink = '/problems/'+ solution.problem_id.slug+'/'
        return HttpResponseRedirect(retlink)
    return render (request, 'problems/edit_solution.html', render_list)