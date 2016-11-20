from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
import views
from problems.views.post_problem_distance import post_problem_disctance

urlpatterns = patterns('',
        url(r'^outdated/$', views.outdated, name='outdated'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^add_problem/$', views.add_problem, name='add_problem'),
        url(r'^problems/(?P<problem_title_slug>[\w\-]+)/$', views.add_solution, name='add_solution'),
        url(r'^accept_solution/(?P<solution_id_slug>[\w\-]+)/$', views.accept_solution, name='accept_solution'),     
        url(r'^own_problems/$', views.own_problems, name='own_problems'),
        url(r'^edit_solution/(?P<solution_id_slug>[\w\-]+)/$', views.edit_solution, name='edit_solution'),
        url(r'^edit_problem/(?P<problem_title_slug>[\w\-]+)/$', views.edit_problem, name='edit_problem'),
        url(r'^post_problem_disctance/$', post_problem_disctance, name='post_problem_disctance'),
        #Urls with Post methods:
        url(r'^users/(?P<user_id_slug>[\w\-]+)/$', views.post_user_ignore, name='users'),
        url(r'^ignored_users/$', views.post_user_unblock, name='post_user_unblock'),
        url(r'^ratings/$', views.post_ratings, name='ratings'),
        
        #TemplateView as views:
        url(r'^about/$', login_required(TemplateView.as_view(template_name="problems/about.html")), name='about'),
        url(r'^outdated/$', login_required(TemplateView.as_view(template_name="problems/outdated.html")), name='outdated'),
        url(r'^$', TemplateView.as_view(template_name="problems/index.html"), name='index'),
        url(r'^notifications', login_required(TemplateView.as_view(template_name="problems/notifications.html")), name='notifications'),
        url(r'^tag/(?P<tag_id_slug>[\w\-]+)/$', login_required(TemplateView.as_view(template_name="problems/tag.html")), name='tag_filter'),        
        url(r'^search/$', login_required(TemplateView.as_view(template_name="problems/search.html")), name='search'),
        url(r'^terms_of_use/$', TemplateView.as_view(template_name="problems/terms_of_use.html"), name='terms_of_use'),
        
        #JSON URLS:
        url(r'^check_the_unchecked_notifications.json', views.check_the_unchecked_notifications),
        url(r'^get_notifications_(?P<count>[\w\-]+).json', views.get_notifications),
        url(r'^get_problems-(?P<deadline>[\w\-]+)-(?P<problem_type>[\w\-]+).json', views.get_problems),
        url(r'^tag_cloud.json', views.tag_cloud),
        url(r'^get_problems_by_tag-(?P<tag_id_slug>[\w\-]+)-(?P<problem_type>[\w\-]+).json', views.get_problems_by_tag, name='get_problems_by_tag'),
        url(r'^get_user_details_by_id-(?P<user_id_slug>[\w\-]+).json', views.get_user_details, name='get_user_details'),
        url(r'^get_problems_by_keyword/$', views.get_problems_by_keyword, name='get_problems_by_keyword'),
        url(r'^get_users_by_keyword/$', views.get_users_by_keyword, name='get_users_by_keyword'),
        url(r'^get_ignored_users.json', views.get_ignored_users, name='get_ignored_users'),
        url(r'^get_ratings-(?P<requested_type>[\w\-]+).json', views.get_ratings),
        
        #robots:
        url(r'^robots\.txt$', TemplateView.as_view(template_name="problems/robots.txt"), name='robots.txt'),
)
