from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^studies/', include('studies.urls')),
    url(r'^accounts/', include('researchers.urls')),
    url(r'^jobs/', include('remote_jobs.urls')),    
)
