from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

from researchers.views import AccountLogin, AccountLogout, AccountCreate

urlpatterns = patterns(
    '',
    url(r'^create/$', AccountCreate.as_view(), name='account_create'),
    url(r'^login/$', AccountLogin.as_view(), name='account_login'),
    url(r'^logout/$', AccountLogout.as_view(), name='account_logout'),
)
