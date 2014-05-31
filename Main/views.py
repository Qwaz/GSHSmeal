#encoding: utf-8
from datetime import date

from django.shortcuts import render

from models import Meal
from forms import LoginForm
from utils import update_today


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
			#return
			return
	else:
		form = LoginForm()
	return render(request, 'login.html', {
		'form': form
	})