from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^(?P<food_id>\d+)/$', 'meals.rating.views.food_rating', name='food_rating'),
)
