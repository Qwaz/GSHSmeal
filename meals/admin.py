from django.contrib import admin

from meals.models import Meal, Food


admin.site.register(Meal)
admin.site.register(Food)
