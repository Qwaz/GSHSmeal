#encoding: utf-8
from datetime import date

from django.shortcuts import render, redirect
from django.contrib import messages

from models import Meal
from forms import LoginForm
from utils.update_meal import update_today
from utils.gshs import login_api


# Create your views here.
def home(request):
	update_today()
	return render(request, 'home.html', {
		'meals': Meal.objects.filter(date=date.today()).order_by('meal_type'),
	})


def login(request):
	if 'user_name' in request.session:
		messages.info(request, u'이미 로그인되어 있습니다')
		return redirect('home')

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			login_result = login_api.login(form.cleaned_data['secure_id'], form.cleaned_data['secure_password'], form.cleaned_data['jsession_id'])
			if isinstance(login_result, unicode):
				post_dict = request.POST.copy()
				post_dict['jsession_id'], post_dict['m'] = login_api.get_session_and_m()

				form = LoginForm(post_dict)

				messages.error(request, login_result)
				return render(request, 'login.html', {'form': form})
			else:
				request.session['user_name'] = form.cleaned_data['id']

				messages.success(request, u'로그인에 성공했습니다')
				return redirect('home')
	else:
		form = LoginForm()
		form.fields['jsession_id'].initial, form.fields['m'].initial = login_api.get_session_and_m()

	return render(request, 'login.html', {
		'form': form
	})


def logout(request):
	if 'user_name' in request.session:
		del request.session['user_name']
	else:
		messages.info(request, u'로그인 상태가 아닙니다')

	return redirect('home')