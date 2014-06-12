from django.conf.urls import patterns, include, url

food_patterns = patterns('',
                         url(r'^(?P<food_id>\d+)/$', 'meals.views.food_detail', name='food_detail')
)

urlpatterns = patterns('',
                       url(r'^foods/', include(food_patterns)),
)
