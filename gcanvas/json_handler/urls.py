from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       # ex: /polls/5/
                       #url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
                       url('^people\.json$', views.PeopleJsonView.as_view(), name="people_json"),
                       #static('/', document_root=settings.STATIC_ROOT)
                   )
