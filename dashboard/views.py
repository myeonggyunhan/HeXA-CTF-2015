# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from gameboard.models import Entries, SolverListModel, Categories
from noticeboard.models import NoticeEntries
from account.models import Account
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings

import hashlib
import datetime
import os
import sys

DOWNLOAD_DIR = settings.MEDIA_ROOT

@login_required
def add_problem(request):

	# Check admin
	if not request.user.is_superuser:
		return HttpResponseRedirect("/")

	entry_title = request.POST.get('title', '')
	if not entry_title.strip():
		messages.error(request, "문제명을 입력하세요.")
		return HttpResponseRedirect("/")

	try:
		title_check = Entries.objects.get(title = entry_title)
		messages.error(request, "존재하는 문제의 이름입니다. 다른 문제명을 사용해주세요.")
		return HttpResponseRedirect("/")
	except:
		pass

	try:
		entry_category = Categories.objects.get(title=request.POST['category'])
	except:
		messages.error(request, "등록되지 않은 문제종류입니다.")
		return HttpResponseRedirect("/")

	if request.POST.has_key('point'):
		try:
			entry_point = int(request.POST['point'])
		except:
			messages.error(request,"문제점수는 정수만 가능합니다.")
			return HttpResponseRedirect("/")
	else:
		messages.error(request,"문제점수를 입력하세요.")
		return HttpResponseRedirect("/")


	entry_answer = request.POST.get('answer', '')
	if not entry_answer.strip():
		messages.error(request, "문제정답을 입력하세요.")
		return HttpResponseRedirect("/")

	# answer is saved to md5 format
	try:
		entry_answer = hashlib.md5(entry_answer).hexdigest()
	except:
		messages.error(request, "정답에는 한글이 들어갈수없습니다.")
		return HttpResponseRedirect("/")

	entry_content = request.POST.get('description', '')
	if not entry_content.strip():
		messages.error(request, "문제내용을 입력하세요.")
		return HttpResponseRedirect("/")

	new_entry = Entries(	title=entry_title,
				description=entry_content,
				category=entry_category,
				point=entry_point,
				answer=entry_answer,
				problem_file=request.FILES.get('problem_file',''), 
				is_active=True )

	new_entry.save()
        messages.success(request,"문제를 성공적으로 등록하였습니다.")
        return HttpResponseRedirect('/')
	
@login_required
def add_notice(request):

	# Check admin
	if not request.user.is_superuser:
		return HttpResponseRedirect("/")

	entry_title = request.POST.get('notice_title', '')
	if not entry_title.strip():
		messages.error(request, "공지사항 제목을 입력하세요.")
		return HttpResponseRedirect("/")

	try:
		title_check = Entries.objects.get(title = entry_title)
		messages.error(request, "존재하는 제목명입니다. 다른 제목명을 사용해주세요.")
		return HttpResponseRedirect("/")
	except:
		pass

	entry_content = request.POST.get('notice_description', '')
	if not entry_content.strip():
		messages.error(request, "공지사항 내용을 입력하세요.")
		return HttpResponseRedirect("/")


	new_entry = NoticeEntries(title=entry_title, description=entry_content)

        try:
                new_entry.save()
        except:
                messages.error(request, "공지사항 등록에 실패하였습니다.")
                return HttpResponseRedirect("/")

        messages.success(request,"공지사항을 성공적으로 등록하였습니다.")
        return HttpResponseRedirect('/')

@login_required
def delete_problem(request, prob_id=None):

	# Check admin
	if not request.user.is_superuser:
		return HttpResponseRedirect("/")
	
	if not prob_id:
		return HttpResponseRedirect("/")

	entry = Entries.objects.get(id=prob_id)
	
	# Update solver's score
	solver_list = SolverListModel.objects.filter(problem_id=prob_id)
	for solver in solver_list:
		u = User.objects.get(username = solver.username)
		account = Account.objects.get(user = u)	
		account.score -= (entry.point + solver.breakthru_point)
		account.save()

	# If Attachment exist, then remove it.
	if entry.problem_file:
		filepath = os.path.join(DOWNLOAD_DIR, str(entry.problem_file))
		os.unlink(filepath)

	# re-sort rank
	ranks = Account.objects.all().order_by('-score','last_auth','id')
	my_rank=1
	for rank in ranks:
		rank.rank=my_rank
		rank.save()
		my_rank+=1

	# Delete solver list
	SolverListModel.objects.filter(problem_id = prob_id).delete()

	entry.delete()
	return HttpResponseRedirect("/")

@login_required
def edit_problem(request, prob_id=None):
	# Check admin
	if not request.user.is_superuser:
		return HttpResponseRedirect("/")

	# Get current problem entry
	prob_entry = Entries.objects.get(id = prob_id)

	if request.method == 'POST':
		entry_title = request.POST.get('title', '')
		if not entry_title.strip():
			messages.error(request, "문제명을 입력하세요.")
			return HttpResponseRedirect("/")

		try:
			entry_category = Categories.objects.get(title=request.POST['category'])
		except:
			messages.error(request, "등록되지 않은 문제종류입니다.")
			return HttpResponseRedirect("/")

		if request.POST.has_key('point'):
			try:
				entry_point = int(request.POST['point'])
			except:
				messages.error(request,"문제점수는 정수만 가능합니다.")
				return HttpResponseRedirect("/")
		else:
			messages.error(request,"문제점수를 입력하세요.")
			return HttpResponseRedirect("/")


		# answer is saved to md5 format
		if request.POST.has_key('answer') and len(request.POST['answer']) > 0:
			try:
				entry_answer = request.POST['answer']
				entry_answer = hashlib.md5(entry_answer).hexdigest()
				prob_entry.answer = entry_answer
			except:
				messages.error(request, "정답에는 한글이 들어갈수없습니다.")
				return HttpResponseRedirect("/")

		entry_content = request.POST.get('description', '')
		if not entry_content.strip():
			messages.error(request, "문제내용을 입력하세요.")
			return HttpResponseRedirect("/")


		# 문제 수정하는데 새로운 파일을 등록한 경우
		if request.FILES.has_key('problem_file'):

			# 원래 문제에 첨부파일이 존재했던경우, 원래 파일을 삭제
			if prob_entry.problem_file:
				filepath = os.path.join(DOWNLOAD_DIR, str(prob_entry.problem_file))
				os.unlink(filepath)
			
			prob_entry.problem_file = request.FILES['problem_file']


		# Update solver's score
		solver_list = SolverListModel.objects.filter(problem_id=prob_id)
		for solver in solver_list:
			u = User.objects.get(username = solver.username)
			account = Account.objects.get(user = u)	

			# prob_entry.point is old value, entry_point is new value and we still preserve breakthru-point
			account.score = account.score - prob_entry.point + entry_point
			account.save()

		# re-sort rank
		ranks = Account.objects.all().order_by('-score','last_auth','id')
		my_rank=1
		for rank in ranks:
			rank.rank=my_rank
			rank.save()
			my_rank+=1


		# Update prob_entry
		prob_entry.title = entry_title
		prob_entry.description = entry_content
		prob_entry.category = entry_category
		prob_entry.point = entry_point
			
		try:
			prob_entry.save()
		except:
			messages.error(request, "문제수정에 실패하였습니다.")
			return HttpResponseRedirect("/")

		messages.success(request,"문제를 성공적으로 수정하였습니다.")
		return HttpResponseRedirect("/")

	else:
		categories = Categories.objects.all()
		template = "admin/edit_problem.html"
		return render_to_response(template,locals(),context_instance=RequestContext(request))

@login_required
def delete_notice(request, notice_id=None):

	# Check admin
	if not request.user.is_superuser:
		return HttpResponseRedirect("/")

	if not notice_id:
		return HttpResponseRedirect("/")

	entry = NoticeEntries.objects.get(id=notice_id)
	entry.delete()
	return HttpResponseRedirect("/")

@login_required
def edit_notice(request, notice_id=None):

	# Check admin
	if not request.user.is_superuser:
		return HttpResponseRedirect("/")

	# Get current notice entry	
	notice_entry = NoticeEntries.objects.get(id=notice_id)

	if request.method == 'POST':
		entry_title = request.POST.get('notice_title', '')
		if not entry_title.strip():
			messages.error(request, "공지사항 제목을 입력하세요.")
			return HttpResponseRedirect("/")

		entry_content = request.POST.get('notice_description', '')
		if not entry_content.strip():
			messages.error(request, "공지사항 내용을 입력하세요.")
			return HttpResponseRedirect("/")

		# Update notice
		notice_entry.title = entry_title
		notice_entry.description = entry_content

		try:
			notice_entry.save()
		except:
			messages.error(request, "공지사항 수정에 실패하였습니다.")
			return HttpResponseRedirect("/")

		messages.success(request,"공지사항을 성공적으로 수정하였습니다.")
		return HttpResponseRedirect('/')

	else:	
		template = "admin/edit_notice.html"
		return render_to_response(template,locals(),context_instance=RequestContext(request))
