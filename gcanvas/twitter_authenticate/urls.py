from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

from . import views

urlpatterns = patterns('',
                       url('^login/', views.TwitterAuthView.as_view(), name="default_login"),
                       url('^$', views.TwitterAuthView.as_view(), name="twitter_login"),
                       
                       
                       # Examples:
                       # url(r'^$', 'gcanvas.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       
                       #url(r'^admin/', include(admin.site.urls)),
)
