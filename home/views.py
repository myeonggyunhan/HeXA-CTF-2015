from django.shortcuts import render, render_to_response, RequestContext, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from account.models import Account
from gameboard.models import Categories, Entries, LogEntries, SolverListModel
from noticeboard.models import NoticeEntries

def home(request):

	superuser_flag = False
	try:
		username = request.user.username
		u = User.objects.get(username=request.user.username)
		superuser_flag = u.is_superuser
	except:
		pass
			
	if superuser_flag:
		solver_list = SolverListModel.objects.all()
		categories = Categories.objects.all()
		problem_entries = Entries.objects.all().order_by('category', 'point')
		notice_entries = NoticeEntries.objects.all()
		log_entries = LogEntries.objects.all().order_by('-id')[:50]
		template = "admin/home.html"
	else:  
		template = "home.html"

	return render_to_response(template,locals(),context_instance=RequestContext(request))

