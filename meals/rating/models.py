#encoding: utf-8
from datetime import date, datetime, time, timedelta

from django.db import models
from django.db.models import Avg, Q

from gshs_auth.models import User
from meals.models import Food, Meal, Menu


class Rating(models.Model):
	user = models.ForeignKey(User)
	menu = models.ForeignKey(Menu)

	value = models.IntegerField()


def get_overall_rating(self):
	ret = Rating.objects.filter(menu__food=self).aggregate(Avg('value'))['value__avg']/2

	if ret is None:
		return 0
	return ret


def get_ratable_menu(self, user):
	if not user.is_authenticated():
		return

	yesterday = date.today()-timedelta(days=1)
	today = date.today()
	now_time = datetime.now()

	if now_time.hour >= 21:
		now_meal = 4
	elif now_time.hour >= 18:
		now_meal = 3
	elif now_time.hour >= 12:
		now_meal = 2
	elif now_time.hour >= 7:
		now_meal = 1
	else:
		now_meal = 0

	rated_menu = Rating.objects.filter(user=user).values_list('menu_id', flat=True)

	return Menu.objects.exclude(id__in=rated_menu).filter(
		Q(meal__date=yesterday, meal__meal_type__gt=now_meal) | Q(meal__date=today, meal__meal_type__lte=now_meal),
		food=self
	).order_by('meal__date', 'meal__meal_type')

Food.get_overall_rating = get_overall_rating
Food.get_ratable_menu = get_ratable_menu


def is_ratable(self):
	now_time = datetime.now()

	meal_time = [time(hour=7), time(hour=12), time(hour=18), time(hour=21)][self.meal_type - 1]
	meal_datetime = datetime.combine(self.date, meal_time)

	return now_time >= meal_datetime and now_time-meal_datetime <= timedelta(days=1)

Meal.is_ratable = is_ratable
