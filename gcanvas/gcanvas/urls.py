
from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
                       #url(r'^nationbuilder', include('nationbuilder_connect.urls', namespace='nationbuilder')),
                       url(r'^verify', include('email_verification.urls', namespace='verify')),
                       url(r'^twitter', include('twitter_authenticate.urls', namespace='twitter')),
                       url(r'^accounts', include('gcanvas_user.urls', namespace='accounts')),
                       url(r'^json', include('json_handler.urls', namespace='json')),
                       #url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
                       url(r'.*', include('static_server.urls', namespace='app')),
                       
                       # Examples:
                       # url(r'^$', 'gcanvas.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       
                       #url(r'^admin/', include(admin.site.urls)),
)

