#encoding: utf-8
from django.db import models


# Create your models here.
class Update(models.Model):
	iso_year = models.IntegerField()
	iso_week = models.IntegerField()


class Food(models.Model):
	name = models.CharField(max_length=50)
	allergy = models.IntegerField()

	ALLERGY_SOURCE = (u'아황산염', u'토마토', u'복숭아', u'돼지고기', u'새우', u'게', u'고등어', u'밀', u'대두', u'땅콩', u'메밀', u'우유', u'난류')

	def __unicode__(self):
		return self.name

	def allergy_list(self):
		allergy_list = []

		for i in range(len(self.ALLERGY_SOURCE)):
			if (self.allergy >> i) & 1:
				allergy_list.append(self.ALLERGY_SOURCE[i])

		allergy_list.reverse()
		return allergy_list

	def meals_ordered(self):
		return self.meal_set.order_by('meal_type').order_by('-date')[:5]


class Meal(models.Model):
	date = models.DateField()
	meal_type = models.IntegerField()

	food_from = models.TextField()

	kcal = models.FloatField()
	carbohydrate = models.FloatField()
	protein = models.FloatField()
	fat = models.FloatField()
	vitamin_a = models.FloatField()
	thiamine = models.FloatField()
	riboflavin = models.FloatField()
	vitamin_c = models.FloatField()
	calcium = models.FloatField()
	iron = models.FloatField()

	foods = models.ManyToManyField(Food, through='Menu')

	def __unicode__(self):
		return self.date.strftime('%Y.%m.%d') + ' ' + [u'조식', u'중식', u'석식'][self.meal_type - 1]

	def meal_name(self):
		return ['breakfast', 'lunch', 'dinner'][self.meal_type-1]


class Menu(models.Model):
	food = models.ForeignKey(Food)
	meal = models.ForeignKey(Meal)
