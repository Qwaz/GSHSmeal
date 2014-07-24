#encoding: utf-8
import re

from django.shortcuts import render
from django.http import Http404, HttpResponse

from meals.models import Food, Menu

from meals.rating.models import Rating


def food_rating(request, food_id):
	food = Food.objects.get(id=food_id)
	ratable_menu = food.get_ratable_menu(request.user)

	return render(request, 'food/food_rating.html', {
		'food': food,
	    'ratable_menu': ratable_menu,
	})


def rate_menu(request):
	if request.method == 'POST':
		if request.user.is_authenticated():
			for menu, rating in request.POST.items():
				menu_matches = re.match(r'^menu_(\d+)$', menu)
				rating_matches = re.match(r'^\d(\.5)?$', rating)
				if menu_matches and rating_matches:
					try:
						menu_id = int(menu_matches.group(1))
						menu_rating = float(rating_matches.group(0))

						menu = Menu.objects.get(id=menu_id)

						if 1 <= menu_rating * 2 <= 10 and menu.meal.is_ratable():
							Rating.objects.get_or_create(user=request.user, menu_id=menu_id, defaults={'value': int(menu_rating*2)})
					except (ValueError, Menu.DoesNotExist, Menu.MultipleObjectsReturned):
						pass
		return HttpResponse()
	raise Http404
