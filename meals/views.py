#encoding: utf-8
from datetime import date, datetime, timedelta

from django.shortcuts import render
from django.http import Http404, HttpResponse

from models import Meal, Food
from meals.update_meal import update_meals


def meal_by_date(request, today, is_home):
	day = u"월화수목금토일"[today.weekday()]

	prev_day = Meal.objects.filter(date=today-timedelta(days=1)).first()
	next_day = Meal.objects.filter(date=today+timedelta(days=1)).first()

	return render(request, 'meal.html', {
		'meals': Meal.objects.filter(date=today).order_by('meal_type'),
	    'today': today.strftime('%Y.%m.%d'),
	    'day': day,
	    'prev_day': prev_day.date if prev_day else None,
	    'next_day': next_day.date if next_day else None,
	    'isHome': is_home,
	})


def home(request):
	update_meals()

	return meal_by_date(request, date.today(), is_home=True)


def meal_view(request, date_str):
	try:
		return meal_by_date(request, datetime.strptime(date_str, '%Y-%m-%d').date(), is_home=False)
	except ValueError:
		return Http404


def food_detail(request, food_id):
	food = Food.objects.get(id=food_id)
	now_favorite = food.favorite_by.filter(id=request.user.id).first() is not None

	return render(request, 'food/food_detail.html', {
		'food': food,
	    'now_favorite': now_favorite,
	})


def update_favorite(request):
	food_id = int(request.POST['food_id'])
	add = int(request.POST['add'])

	if request.user.is_authenticated():
		food = Food.objects.get(id=food_id)
		now_favorite = food.favorite_by.filter(id=request.user.id).first() is not None

		if add and not now_favorite:
			food.favorite_by.add(request.user)
		elif not add and now_favorite:
			food.favorite_by.remove(request.user)

	return HttpResponse()
