#encoding: utf-8
from datetime import date

from django.shortcuts import render, redirect

from models import Meal
from forms import LoginForm
from utils import update_today
from Songjuk import login_api


# Create your views here.
def home(request):
	update_today()
	return render(request, 'home.html', {
		'meals': Meal.objects.filter(date=date.today()).order_by('meal_type'),
	})


def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			login_result = login_api.login(form.cleaned_data['secure_id'], form.cleaned_data['secure_password'], form.cleaned_data['jsession_id'])
			if isinstance(login_result, unicode):
				post_dict = request.POST.copy()
				post_dict['jsession_id'], post_dict['m'] = login_api.get_session_and_m()

				form = LoginForm(post_dict)

				return render(request, 'login.html', {
					'form': form,
				    'message_type': 'danger',
				    'message': login_result,
				})
			else:
				return redirect('home')
	else:
		form = LoginForm()
		form.fields['jsession_id'].initial, form.fields['m'].initial = login_api.get_session_and_m()

	return render(request, 'login.html', {
		'form': form
	})