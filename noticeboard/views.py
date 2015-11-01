from django.shortcuts import render,RequestContext, render_to_response
from django.contrib.auth.decorators import login_required
from noticeboard.models import NoticeEntries

@login_required
def notice_view(request):
	template = "notice.html"
	notice_active = "active"
	entries= NoticeEntries.objects.all().order_by('-id')
	return render_to_response(template,locals(),context_instance=RequestContext(request))	
	
