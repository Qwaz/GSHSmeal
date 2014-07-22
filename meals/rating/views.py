import time

from django.shortcuts import render

from meals.models import Food
# Create your views here.
def food_rating(request, food_id):
	time.sleep(1)
	food = Food.objects.get(id=food_id)
	return render(request, 'food/food_rating.html', {
		'food': food
	})
