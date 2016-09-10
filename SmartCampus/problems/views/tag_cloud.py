from problems.models import Tag
from django.db.models import Count
import random
from django.http.response import HttpResponse
import json


def tag_cloud(request):    
    tags = Tag.objects.all()
    if (tags.count()<1):
        return  
    MAX_WEIGHT = 5
    tags = Tag.objects.annotate(count = Count('problems'))
    tags = tags.annotate(weight = Count('problems'))
    
    try:
        max_count_tag = tags.latest('count')
        min_count_tag = tags.earliest('count')
    except:
        pass
    min_count = min_count_tag.count
    max_count = max_count_tag.count

    tag_range = float(max_count - min_count)
    if tag_range == 0.0:
        tag_range = 1.0
    for tag in tags:
        tag.weight = int(MAX_WEIGHT * (tag.count - min_count) / tag_range)
        
    tags = list(tags)
    random.shuffle(tags)
    json_list = []
    for tag in tags:
        json_list.append({'text':tag.tag_text,
                          'weight':tag.weight,
                          'link': "/tag/"+tag.slug,
                          })
    return HttpResponse(json.dumps(json_list, ensure_ascii=False).encode('utf8'))