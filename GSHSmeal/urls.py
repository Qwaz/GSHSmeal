from django.conf.urls import patterns, include, url
from django.contrib import admin

from Main.Food import urls as food_urls


admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', 'Main.views.home', name='home'),
                       url(r'^login/$', 'Main.views.login', name='login'),
                       url(r'^logout/$', 'Main.views.logout', name='logout'),
                       url(r'^foods/', include(food_urls)),
)
