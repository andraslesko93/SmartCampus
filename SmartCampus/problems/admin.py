from django.contrib import admin
from problems.models import  Solution, Ignore, Problem, UserProfile

class ProblemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}

# Register your models here.

admin.site.register(Solution)
admin.site.register(Ignore)
admin.site.register(UserProfile)
admin.site.register(Problem, ProblemAdmin)