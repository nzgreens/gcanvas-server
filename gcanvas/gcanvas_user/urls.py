from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

from . import views

urlpatterns = patterns('',
                       url('user.json$', views.GCanvasUserView.as_view(), name="user"),
                       url('login/.*', views.GCanvasLoginView.as_view(), name="login"),
                       url('register', views.GCanvasRegisterView.as_view(), name="register"),
                       
                       
                       # Examples:
                       # url(r'^$', 'gcanvas.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       
                       #url(r'^admin/', include(admin.site.urls)),
)
