from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

from remote_jobs.views import RemoteJobDetail, RemoteJobList, RemoteJobCreate, RemoteJobUpdate, RemoteJobDelete

urlpatterns = patterns(
    '',
    url(r'^$', RemoteJobList.as_view(), name="remote_job_list"),
    url(r'^(?P<pk>[0-9]+)/$', RemoteJobDetail.as_view(), name='remote_job_detail'),
    url(r'^add/$', RemoteJobCreate.as_view(), name="remote_job_add"),
    url(r'^(?P<pk>[0-9]+)/update$', RemoteJobUpdate.as_view(), name="remote_job_update"),
    url(r'^(?P<pk>[0-9]+)/delete/$', RemoteJobDelete.as_view(), name='remote_job_delete'),
)
