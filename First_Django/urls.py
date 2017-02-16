from django.conf.urls import include, url
from django.contrib import admin
from inventory import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib.auth.views import (password_reset, password_reset_done,
                                      password_reset_confirm, password_reset_complete, password_change,
                                      password_change_done,)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^item/(?P<id>\d+)/', views.item_detail, name="item_detail"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', views.login),
    url(r'^accounts/auth/$', views.auth_view),
    url(r'^accounts/logout/$', views.logout),
    url(r'^accounts/loggedin/$', views.loggedin),
    url(r'^accounts/invalid/$', views.invalid_login),
    url(r'^accounts/register/$', views.register_user),
    url(r'^accounts/register_check/$', views.register_check),
    url(r'^accounts/register_verification/$', views.register_verification),
    #url(r'^items/add_comment/(?P<id>\d+)/$', views.add_comment),
    url(r'^profile/$', views.profile),
    url(r'^edit_profile/$', views.edit_profile),
    url(r'^create/$', views.create),
    url(r'^reset-password/$', password_reset, name='reset-password'),
    url(r'^reset-password/done/$', password_reset_done, name= 'password_reset_done'),
    url(r'^reset-password/complete/$', password_reset_complete, name= 'password_reset_complete'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm, name= 'password_reset_confirm'),
    url(r'^password/change/$', password_change, name='password_change'),
    url(r'^password/change/done/$', password_change_done, name='password_change_done'),
]
if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)