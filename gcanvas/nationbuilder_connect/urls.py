from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

from . import views

urlpatterns = patterns('',
                       url('^$', views.NationBuilderConnectView.as_view(), name="connect"),
                       url('callback', views.NationBuilderConnectView.as_view(), name="callback"),
                       
                       # Examples:
                       # url(r'^$', 'gcanvas.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       
                       #url(r'^admin/', include(admin.site.urls)),
)
