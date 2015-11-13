from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'), 
        url(r'^outdated/$', views.outdated, name='outdated'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^ignored_users/$', views.ignored_users, name='ignored_users'),
        url(r'^add_problem/$', views.add_problems, name='add_problem'), 
        url(r'^own_problems/$', views.own_problems, name='own_problems'),  
        url(r'^add_solution/(?P<problem_title_slug>[\w\-]+)/$', views.add_solution, name='add_solution'),
        url(r'^accept_solution/(?P<solution_id_slug>[\w\-]+)/$', views.accept_solution, name='accept_solution'),
        url(r'^users/(?P<user_id_slug>[\w\-]+)/$', views.list_users, name='users'),
        url(r'^tag/(?P<tag_id_slug>[\w\-]+)/$', views.tag_search, name='tag_search'),
        url(r'^notification/$', views.list_notification, name='notification'),
        url(r'^search/$', views.search, name='search'),
        url(r'^rate/$', views.rate, name='rate'),
        
)
