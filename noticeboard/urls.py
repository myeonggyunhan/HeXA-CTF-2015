from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'noticeboard.views.notice_view'),
)

