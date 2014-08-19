from django.contrib import admin

from meals.models import Meal, Food, Menu


admin.site.register(Meal)
admin.site.register(Food)
admin.site.register(Menu)
