from datetime import date

from django.shortcuts import render

from models import Meal
from utils.update_meal import update_today


# Create your views here.
def home(request):
	update_today()
	return render(request, 'home.html', {
		'meals': Meal.objects.filter(date=date.today()).order_by('meal_type'),
	})
