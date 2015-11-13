import datetime
from haystack import indexes
from problems.models import Problem


class ProblemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    #author = indexes.CharField(model_attr='user')
    added_at = indexes.DateTimeField(model_attr='pub_date')
    
    content_auto = indexes.EdgeNgramField(model_attr = 'title')

    def get_model(self):
        return Problem

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all() #filter(pub_date__lte=datetime.datetime.now())