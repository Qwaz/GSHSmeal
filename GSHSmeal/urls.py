from django.conf.urls import patterns, include, url
from django.contrib import admin

from meals.foods import urls as food_urls


admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', 'meals.views.home', name='home'),
                       url(r'^accounts/login/$', 'gshs_auth.views.login_view', name='login'),
                       url(r'^accounts/logout/$', 'gshs_auth.views.logout_view', name='logout'),
                       url(r'^foods/', include(food_urls)),
)
