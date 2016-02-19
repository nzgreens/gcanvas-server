from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

from . import views

from django.views.decorators.csrf import csrf_exempt, csrf_protect, requires_csrf_token,  ensure_csrf_cookie

urlpatterns = patterns('',
                       url('^user.json$', views.GCanvasUserView.as_view(), name="user"),
                       url('^login$', views.GCanvasLoginView.as_view(), name="login"),
                       url('^logout', views.GCanvasLogoutView.as_view(), name="logout"),
                       url('^register$', views.GCanvasRegisterView.as_view(), name="register"),
                       url('^verify/(?P<code>\w+)$', views.GCanvasVerificationView.as_view(), name="verification"),
                       
                       
                       # Examples:
                       # url(r'^$', 'gcanvas.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       
                       #url(r'^admin/', include(admin.site.urls)),
)
