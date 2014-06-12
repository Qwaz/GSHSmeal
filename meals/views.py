from datetime import date

from django.shortcuts import render

from models import Meal, Food
from utils.update_meal import update_today


# Create your views here.
def home(request):
	update_today()
	return render(request, 'home.html', {
		'meals': Meal.objects.filter(date=date.today()).order_by('meal_type'),
	})


def food_detail(request, food_id):
	food = Food.objects.get(id=food_id)
	return render(request, 'food/food_detail.html', {
		'food': food
	})
