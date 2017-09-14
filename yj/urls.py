from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'yj.views.home'),
    url(r'^api/', include('api.urls')),
    
    # Include an application:
    # url(r'^app_name/', include('app_name.urls', namespace="app_name")),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
