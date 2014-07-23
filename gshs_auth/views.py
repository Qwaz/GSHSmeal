#encoding: utf-8

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from gshs_auth.forms import LoginForm
from gshs_auth import login_api


def login_view(request):
	redirect_to = request.REQUEST.get('next', '/')

	if request.user.is_authenticated():
		messages.info(request, u'이미 로그인되어 있습니다')
		return HttpResponseRedirect(redirect_to)

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			clean = form.cleaned_data
			user = authenticate(
				username=clean['id'],
				rsa_id=clean['secure_id'],
				rsa_password=clean['secure_password'],
				jsession_id=clean['jsession_id'],
				request=request,
			)

			if user is not None and user.is_active:
				login(request, user)

				messages.success(request, u'로그인에 성공했습니다')
				return redirect('home')
			else:
				post_dict = request.POST.copy()
				post_dict['jsession_id'], post_dict['m'] = login_api.get_session_and_m()

				form = LoginForm(post_dict)
	else:
		form = LoginForm()
		form.fields['jsession_id'].initial, form.fields['m'].initial = login_api.get_session_and_m()

	return render(request, 'login.html', {
		'form': form,
	    'redirect_to': redirect_to,
	})


def logout_view(request):
	if request.user.is_authenticated():
		logout(request)
		messages.info(request, u'로그아웃 되었습니다')
	else:
		messages.warning(request, u'로그인 상태가 아닙니다')

	return redirect('home')
