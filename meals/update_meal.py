#encoding: utf-8
from datetime import date, datetime, timedelta
import re

from django.db import transaction
from bs4 import BeautifulSoup, Tag
import requests

from meals.models import Update, Food, Meal, Menu
from utils.iso_calendar import iso_to_gregorian


class MealSet():
	def __init__(self, meal_type):
		self._meal_count = 0
		self.meals = []
		self.foods = []

		for i in range(7):
			self.meals.append(Meal())
			self.meals[i].meal_type = meal_type
			self.foods.append([])

	def _count_step(self):
		self._meal_count += 1
		if self._meal_count == 7:
			self._meal_count = 0

	def set_timestamp(self, data):
		setattr(self.meals[self._meal_count], 'date', datetime.strptime(data[0:10], "%Y.%m.%d").date())
		self._count_step()

	def set_foods(self, data):
		for food_name in data.split('<br/>')[:-1]:
			allergy = 0
			allergy_mark = u'⑬⑫⑪⑩⑨⑧⑦⑥⑤④③②①'
			for i in range(len(allergy_mark)):
				if food_name[-1] == allergy_mark[i]:
					allergy ^= 1 << i
					food_name = food_name[:-1]

			food_name = re.sub(ur'([\-=*]|\((초|중|고|조|주식)\))*$', '', food_name)
			food_name = re.sub(r'[0-9]+', '', food_name)

			food = Food.objects.get_or_create(name=food_name, allergy=allergy)[0]
			self.foods[self._meal_count].append(food)
		self._count_step()

	def set_etc(self, column_name, data):
		if column_name == 'food_from':
			setattr(self.meals[self._meal_count], column_name, data)
		else:
			try:
				setattr(self.meals[self._meal_count], column_name, float(data))
			except ValueError:
				setattr(self.meals[self._meal_count], column_name, 0.0)
		self._count_step()

	def save(self):
		for i in range(7):
			self.meals[i].save()
			for food in self.foods[i]:
				menu = Menu.objects.create(food=food, meal=self.meals[i])


@transaction.atomic
def update_meal(meal_date):
	iso_calendar = meal_date.isocalendar()

	obj, created = Update.objects.get_or_create(iso_year=iso_calendar[0], iso_week=iso_calendar[1])

	if created:
		for i in range(1, 4):
			payload = {'insttNm': u'경기과학고등학교', 'schulCode': 'J100000447', 'schulCrseScCode': '4',
			           'schulKndScCode': '04'}
			payload['schYmd'] = meal_date.strftime("%Y.%m.%d")
			payload['schMmealScCode'] = str(i)
			r = requests.post('http://hes.goe.go.kr/sts_sci_md01_001.do', payload)

			soup = BeautifulSoup(r.text)

			ms = MealSet(i)
			row_func = {
				0: ms.set_timestamp, 2: ms.set_foods, 15: ms.set_etc,
				17: ms.set_etc, 18: ms.set_etc, 19: ms.set_etc, 20: ms.set_etc, 21: ms.set_etc,
				22: ms.set_etc, 23: ms.set_etc, 24: ms.set_etc, 25: ms.set_etc, 26: ms.set_etc
			}

			row_args = {
				15: 'food_from', 17: 'kcal', 18: 'carbohydrate', 19: 'protein',
				20: 'fat', 21: 'vitamin_a', 22: 'thiamine', 23: 'riboflavin',
				24: 'vitamin_c', 25: 'calcium', 26: 'iron'
			}

			row_count = 0
			tr_count = len(soup.findAll('tr'))

			for row in soup.findAll('tr'):
				if tr_count < 27 and row_count == 2:
					row_count += 1

				for data in (row.findAll('th') + row.findAll('td'))[1:]:
					a = data.contents
					if len(a):
						tmp_text = u''.join(map(lambda x: unicode(x) if type(x) == Tag else x, a))
					else:
						tmp_text = ''

					if row_count in row_func:
						if row_count in row_args:
							row_func[row_count](data=tmp_text, column_name=row_args[row_count])
						else:
							row_func[row_count](data=tmp_text)
				row_count += 1

			ms.save()


def update_meals():
	start_iso = Update.objects.order_by('-iso_year', '-iso_week').first()
	if start_iso is None:
		start_iso = date.today().isocalendar()[:2]
	else:
		start_iso = (start_iso.iso_year, start_iso.iso_week)

	now = iso_to_gregorian(start_iso[0], start_iso[1], 1)

	last_iso = (date.today()+timedelta(days=1)).isocalendar()[:2]
	last = iso_to_gregorian(last_iso[0], last_iso[1], 1)

	while now <= last:
		update_meal(now)
		now += timedelta(days=7)
