from django.contrib import admin

from meals.models import Meal, Food, Menu


class FoodAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']


admin.site.register(Meal)
admin.site.register(Food, FoodAdmin)
admin.site.register(Menu)
