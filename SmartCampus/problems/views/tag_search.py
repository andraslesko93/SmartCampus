from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from problems.models import Problem, Tag


@login_required
def tag_search(request, tag_id_slug):
    try:
        problems = Problem.objects.all()
        tag = Tag.objects.all()
        tag = tag.filter (slug = tag_id_slug)
        problems = problems.filter(tags = tag)
    except Problem.DoesNotExist:
        pass
    context_dict = {'problems': problems}
    return render(request, 'problems/tag.html', context_dict)
