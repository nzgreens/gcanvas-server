from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       url('^$', views.GCanvasView.as_view()),
                       #static('/', document_root=settings.STATIC_ROOT)
                   )
