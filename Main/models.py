#encoding: utf-8
from django.db import models


# Create your models here.
class Update(models.Model):
	iso_year = models.IntegerField()
	iso_week = models.IntegerField()


class Food(models.Model):
	name = models.CharField(max_length=50)
	allergy = models.IntegerField()


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

	foods = models.ManyToManyField(Food)

	def __unicode__(self):
		return self.date.strftime('%Y.%m.%d') + ' ' + [u'조식', u'중식', u'석식'][self.meal_type - 1]
