from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^(?P<food_id>\d+)/$', 'meals.foods.views.food_detail', name='food_detail')
)
