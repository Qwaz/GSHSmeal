from django.shortcuts import render

from meals.models import Food


def food_rating(request, food_id):
	food = Food.objects.get(id=food_id)
	return render(request, 'food/food_rating.html', {
		'food': food
	})
