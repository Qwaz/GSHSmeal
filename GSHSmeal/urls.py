from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', 'Main.views.home', name='home'),
                       url('^login/$', 'Main.views.login', name='login'),
                       url('^logout/$', 'Main.views.logout', name='logout')
)
