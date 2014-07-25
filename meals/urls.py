from django.conf.urls import patterns, include, url

from rating import urls as rating_urls


food_patterns = patterns('',
                         url(r'^(?P<food_id>\d+)/$', 'meals.views.food_detail', name='food_detail')
)

urlpatterns = patterns('',
                       url(r'^foods/', include(food_patterns)),
                       url(r'^rating/', include(rating_urls)),
                       url(r'^(\d{4}-\d{2}-\d{2})/$', 'meals.views.meal_view', name='meal_view')
)
