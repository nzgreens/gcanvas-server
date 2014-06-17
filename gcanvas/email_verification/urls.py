from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

from . import views

urlpatterns = patterns('',
                       url('^$', views.EmailVerifierRESTView.as_view(), name="email_verifier"),
                       
                       
                       # Examples:
                       # url(r'^$', 'gcanvas.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       
                       #url(r'^admin/', include(admin.site.urls)),
)
