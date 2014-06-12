from django.conf.urls import patterns, include, url
from django.contrib import admin

from meals.foods import urls as food_urls
from gshs_auth.decorators import admin_login


admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', 'meals.views.home', name='home'),
                       url(r'^accounts/login/$', 'gshs_auth.views.login_view', name='login'),
                       url(r'^accounts/logout/$', 'gshs_auth.views.logout_view', name='logout'),
                       url(r'^foods/', include(food_urls)),
)

admin.site.login = admin_login(admin.site.login)
