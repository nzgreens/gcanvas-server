from django.contrib.auth import views as auth_views
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       #url(r'^nationbuilder', include('nationbuilder_connect.urls', namespace='nationbuilder')),
                       url(r'^verify/', include('email_verification.urls', namespace='verify')),
                       url(r'^twitter/', include('twitter_authenticate.urls', namespace='twitter')),
                       url(r'^accounts/', include('gcanvas_user.urls', namespace='accounts')),
                       url(r'^json/', include('json_handler.urls', namespace='json')),
                       url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
                       
                       
                       
                       # Examples:
                       # url(r'^$', 'gcanvas.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^admin/login/', include(admin.site.urls)),
                       

                       url(r'^admin/password_reset/$', auth_views.password_reset, name='admin_password_reset'),
                       url(r'^admin/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
                       url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
                       url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
                       url(r'.*', include('static_server.urls', namespace='app')),
)

