from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CreateForm, AuthForm
from .models import Account
from django.contrib.auth.models import User

def sign_in(request):
        auth_form = AuthForm(data = request.POST or None)
        template = 'account/sign_in.html'
        next_url = request.POST.get("next", "/")

        if request.method == 'POST':
                if auth_form.is_valid():
                        login(request, auth_form.get_user())
                        return redirect(next_url)
                else:
                        messages.error(request, "Incorrect username or password!")
                        return render(request, template, {'signin_form':auth_form, 'next':next_url, })

        return render(request, template, {'signin_form':auth_form, 'next':next_url, })

def sign_up(request):
        create_form = CreateForm(data = request.POST or None)
        template = 'account/sign_up.html'
        next_url = request.POST.get("next", "/")

        if request.method == 'POST':

		# If not register period, then redirect to root and send message.
		if not settings.IS_REGISTER_PERIOD:
			return HttpResponse("<script>alert('You can register after CTF start :)');location.href='/';</script>")

                if create_form.is_valid():
                        username = create_form.clean_username()
                        password = create_form.clean_password2()
                        new_user = create_form.save()

			# Update new user's rank
			u = User.objects.get(username=username)
			new_account = Account.objects.get(user=u)
			new_rank = Account.objects.count()
			new_account.rank = new_rank
			new_account.save()

                        user = authenticate(username=username, password=password)
                        login(request, user)

                        return redirect(next_url)
                else:
			error_message = '<div class="header">There was some errors with your submission</div>'
			error_message+= '<ul class="list">'
			error_message+= '<li>Try other username.</li>'
			error_message+= '<li>Password and Password confirm must be the same.</li>'
			error_message+= '</ul>'
                        messages.error(request, error_message)
                        return render(request, template, {'signup_form':create_form, 'next':next_url, })

        return render(request, template, {'signup_form':create_form, 'next':next_url, })


@login_required
def sign_out(request):
        logout(request)
        return redirect("/")

