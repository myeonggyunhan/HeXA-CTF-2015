from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'gameboard.views.index'),
	url(r'^scoreboard/$', 'gameboard.views.scoreboard'),
	url(r'^prob_view/(?P<prob_id>\d+)/$', 'gameboard.views.prob_view'),
	url(r'^auth/(?P<prob_id>\d+)/$', 'gameboard.views.auth'),
	url(r'^download/(?P<prob_id>\d+)/$', 'gameboard.views.download'),

)

