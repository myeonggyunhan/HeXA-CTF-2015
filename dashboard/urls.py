from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

        url(r'^add_problem/$', 'dashboard.views.add_problem'),
        url(r'^add_notice/$', 'dashboard.views.add_notice'),
	url(r'^delete_problem/(?P<prob_id>\d+)/$', 'dashboard.views.delete_problem'),
	url(r'^edit_problem/(?P<prob_id>\d+)/$', 'dashboard.views.edit_problem'),
	url(r'^delete_notice/(?P<notice_id>\d+)/$', 'dashboard.views.delete_notice'),
	url(r'^edit_notice/(?P<notice_id>\d+)/$', 'dashboard.views.edit_notice'),
)

