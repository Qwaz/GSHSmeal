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
	type = models.IntegerField()

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
