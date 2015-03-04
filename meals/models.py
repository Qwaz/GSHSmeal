from django.db import models

from gshs_auth.models import User


class Update(models.Model):
    iso_year = models.IntegerField()
    iso_week = models.IntegerField()


class Food(models.Model):
    name = models.CharField(max_length=50)
    allergy = models.IntegerField(default=0)

    favorite_by = models.ManyToManyField(User, related_name='favorites', blank=True)

    is_snack = models.BooleanField(default=False)

    ALLERGY_SOURCE = ('아황산염', '토마토', '복숭아', '돼지고기', '새우', '게', '고등어', '밀', '대두', '땅콩', '메밀', '우유', '난류')

    def __str__(self):
        return self.name

    def allergy_list(self):
        allergy_list = []

        for i in range(len(self.ALLERGY_SOURCE)):
            if (self.allergy >> i) & 1:
                allergy_list.append(self.ALLERGY_SOURCE[i])

        allergy_list.reverse()
        return allergy_list

    def meals_ordered(self):
        return self.meal_set.order_by('-date', 'meal_type')[:5]


class Meal(models.Model):
    MEAL_TYPE_CHOICES = (
        (1, '조식'),
        (2, '중식'),
        (3, '석식'),
        (4, '간식'),
    )

    date = models.DateField()
    meal_type = models.IntegerField(choices=MEAL_TYPE_CHOICES)

    food_from = models.TextField(blank=True)

    kcal = models.FloatField(default=0)
    carbohydrate = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    vitamin_a = models.FloatField(default=0)
    thiamine = models.FloatField(default=0)
    riboflavin = models.FloatField(default=0)
    vitamin_c = models.FloatField(default=0)
    calcium = models.FloatField(default=0)
    iron = models.FloatField(default=0)

    foods = models.ManyToManyField(Food, through='Menu')

    def __str__(self):
        return self.date.strftime('%Y.%m.%d') + ' ' + ['조식', '중식', '석식', '간식'][self.meal_type - 1]

    def meal_name(self):
        return ['breakfast', 'lunch', 'dinner', 'snack'][self.meal_type-1]


class Menu(models.Model):
    food = models.ForeignKey(Food)
    meal = models.ForeignKey(Meal)

    def __str__(self):
        return self.meal+' - '+self.food
