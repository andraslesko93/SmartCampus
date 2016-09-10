from django.contrib import admin
from problems.models import  Solution, Ignore, Problem, UserProfile, Tag, Rating, Notification,\
    Confidence_Problem

class ProblemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}


# Register your models here.

admin.site.register(Solution)
admin.site.register(Ignore)
admin.site.register(UserProfile)
admin.site.register(Tag)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Rating)
admin.site.register(Notification)
admin.site.register(Confidence_Problem)