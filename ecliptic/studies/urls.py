from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

from studies.views import StudyDetail, StudyList, StudyCreate, StudyUpdate, StudyDelete

urlpatterns = patterns(
    '',
    url(r'^$', StudyList.as_view(), name="study_list"),
    url(r'^(?P<pk>[0-9]+)/$', StudyDetail.as_view(), name='study_detail'),
    url(r'^add/$', StudyCreate.as_view(), name="study_add"),
    url(r'^(?P<pk>[0-9]+)/update$', StudyUpdate.as_view(), name="study_update"),
    url(r'^(?P<pk>[0-9]+)/delete/$', StudyDelete.as_view(), name='study_delete'),
)
