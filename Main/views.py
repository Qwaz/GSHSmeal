#encoding: utf-8
from datetime import date

from django.shortcuts import render

from models import Meal
from utils import update_today


# Create your views here.
def home(request):
	return render(request, 'home.html', {
		'meals': Meal.objects.filter(date=date.today()).order_by('meal_type'),
	})

from django.http import HttpResponse


def test(request):
	update_today()
	return HttpResponse('updated')