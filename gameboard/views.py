# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from gameboard.models import Entries, LogEntries, SolverListModel, Categories
from account.models import Account
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.core.servers.basehttp import FileWrapper
from django.http import StreamingHttpResponse
import mimetypes

import hashlib
import datetime
import os

DOWNLOAD_DIR = settings.MEDIA_ROOT

@login_required
def index(request):
	template = "gameboard.html"

	# Load all problem entries
	category_list = list(Categories.objects.all())
	problem_entry_dict = dict()
	for category in category_list:
		problem_entry_dict[category.title] = list(Entries.objects.filter(category = category).order_by('point'))

	# Load current user solved problems
	solver_list = SolverListModel.objects.filter(username = request.user.username)
	solved_problem_list = []
	for solver in solver_list:
		solved_problem_list.append(solver.problem_id) 

	return render_to_response(template,locals(),context_instance=RequestContext(request))

# Scoreboard can see anybody
# @login_required
def scoreboard(request):
	template = "scoreboard.html"
        ranks = Account.objects.all().order_by('-score','last_auth','id')

	if (not request.user.is_superuser) and (not request.user.is_anonymous()):
        	u = User.objects.get(username = request.user.username)
	        current_user = Account.objects.get(user=u)

        return render_to_response(template,locals(),context_instance=RequestContext(request))

@login_required
def prob_view(request, prob_id=None):
	if prob_id:
		template = "taskviewer.html"
		prob_entry = Entries.objects.get(id=prob_id)
	else:
		template = "taskviewer_empty.html"

	return render_to_response(template,locals(),context_instance=RequestContext(request))

@login_required
def download(request, prob_id=None):
	# TODO: Send error message to user
	if not prob_id:
		return HttpResponseRedirect("/gameboard/")
	
	prob_entry = Entries.objects.get(id = prob_id)
	prob_file = str(prob_entry.problem_file)

	filename = os.path.join(DOWNLOAD_DIR, prob_file)
	chunk_size = 8192
	response = StreamingHttpResponse(FileWrapper(open(filename), chunk_size), content_type='application/octet-stream')
	response['Content-Length'] = os.path.getsize(filename)
	response['Content-Disposition'] = "attachment; filename=\"%s\"" % os.path.basename(filename)
	return response


@login_required
def auth(request, prob_id=None):

	try:
		prob_entry=Entries.objects.get(id = int(prob_id))
	except:
		messages.error(request, "해당 문제가 존재하지않습니다.")
		return HttpResponseRedirect("/gameboard/")

	user_answer = request.POST.get('answer', '')
	try:
		user_answer = str(user_answer)
	except:
		messages.error(request, "정답에는 한글이 들어갈 수 없습니다.")
		return HttpResponseRedirect("/gameboard/")

	# Compare user anser and real answer
	user_answer = hashlib.md5(user_answer).hexdigest()

	# If admin, then check answer but don't update score.
	# It is only for test. Flag checking purpose.
	if request.user.is_superuser:
		if prob_entry.is_active:
			messages.success(request, "Problem is activated")
		else:
			messages.error(request, "Problem is not activated")

		if prob_entry.answer != user_answer:
			messages.error(request, "Admin debugging mode... Wrong Answer!")
		else:
			messages.success(request, "Admin debugging mode... Correct Answer!")

		return HttpResponseRedirect("/gameboard/")


	u = User.objects.get(username=request.user.username)
	current_account = Account.objects.get(user = u)

	if prob_entry.answer != user_answer:
		
		if prob_entry.is_active:
			# e.g. User 'leap' System 300 - HeCHO problem auth failed.
			log_desc = "%s %d - '%s' problem auth failed." % (prob_entry.category.title, prob_entry.point, prob_entry.title)
			new_log = LogEntries(account = current_account, description = log_desc)
			new_log.save()
		
		messages.error(request, "Wrong Answer!")
		return HttpResponseRedirect("/gameboard/")

	username = str(request.user.username)
	try:
		solver = SolverListModel.objects.get(username=username, problem_id=prob_entry.id)
		message = "You already cleared "
		message += str(prob_entry.category.title) +" "
		message += str(prob_entry.point) +" - "
		message += str(prob_entry.title) + ". "
		messages.error(request, message)
		return HttpResponseRedirect("/gameboard/")

	except:
		if not prob_entry.is_active:
			message = "Correct answer! But you can't get any points because CTF is over :("
			messages.success(request, message)
			return HttpResponseRedirect("/gameboard/")

		breakthru = prob_entry.solver_list.count()
		breakthru_point = 0
		if breakthru < 3:
			breakthru_point += (3 - breakthru)

		# Add to SolverList and update solve counter
		solver = SolverListModel.objects.create(username=username, problem_id=prob_entry.id, breakthru_point=breakthru_point)
		solve_cnt = int(prob_entry.solver_count)+1
		prob_entry.solver_count = solve_cnt
		prob_entry.solver_list.add(solver)
		prob_entry.save()

		# update user score
		u = User.objects.get(username=request.user.username)
		current_user = Account.objects.get(user=u)
		current_user.score += int(prob_entry.point)
		current_user.score += int(breakthru_point)

		# update user last_auth time
		current_user.last_auth = datetime.datetime.now()
		current_user.save()

		# update user rank
		ranks = Account.objects.all().order_by('-score','last_auth','id')
		my_rank=1
		for rank in ranks:
			rank.rank=my_rank
			rank.save()
			my_rank+=1

		# Congratulation message
		message = "Congratulations! You cleared "
		message += str(prob_entry.category.title) +" "
		message += str(prob_entry.point) +" - "
		message += str(prob_entry.title) + ". "
		message += " You got  " + str(prob_entry.point) + " Points."

		# User 'leap' System 300 - HeCHO problem auth success.
		log_desc = "%s %d - '%s' problem auth success." % (prob_entry.category.title, prob_entry.point, prob_entry.title)
		new_log = LogEntries(account = current_account, description = log_desc)
		new_log.save()

		messages.success(request, message)
		return HttpResponseRedirect("/gameboard/")

