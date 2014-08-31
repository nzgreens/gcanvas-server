import json

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.http import HttpResponse, Http404
from django.conf import settings


from .authenticator import OAuthSession, NationUserManager


class NationBuilderConnectView(View):
    def __init__(self, *args, **kwargs):
        super(NationBuilderConnectView, self).__init__(*args, **kwargs)
        client_id=settings.NATIONBUILDER_CLIENT_ID
        client_secret=settings.NATIONBUILDER_CLIENT_SECRET
        client_name=settings.NATIONBUILDER_CLIENT_NAME
        redirect_url=settings.NATIONBUILDER_CLIENT_CALLBACK
        self._oauthsession = OAuthSession(
            client_id,
            client_secret,
            client_name,
            redirect_url
        )

        self._nationmanager = NationUserManager()

    def get(self, request, *args, **kwargs):
        if len(request.GET) > 0:
            if 'code' in request.GET:
                code = request.GET['code']
                token = self._oauthsession.get_access_token(code)
                                
                nationuser = self._nationmanager.create_nation_user(self._oauthsession, token)
                self._nationmanager.login(request, nationuser.nation_user_id)
                
                return redirect('/')
            else:
                return HttpResponse(json.dumps(request.GET), content_type='application/json')
        
        if not request.user.is_authenticated() or not self._nationmanager.is_nation_user(request.user):
            return redirect(self._oauthsession.get_authorisation_url())

        #@TODO: fix this up to stop a neverending loop of redirects.
        return redirect(reverse('app:main'), register=True, permanent=True)


class NationBuilderListsView(View):
    def __init__(self, *args, **kwargs):
        super(NationBuilderListsView, self).__init__(*args, **kwargs)
        client_id=settings.NATIONBUILDER_CLIENT_ID
        client_secret=settings.NATIONBUILDER_CLIENT_SECRET
        client_name=settings.NATIONBUILDER_CLIENT_NAME
        redirect_url=settings.NATIONBUILDER_CLIENT_CALLBACK
        self._oauthsession = OAuthSession(
            client_id,
            client_secret,
            client_name,
            redirect_url
        )


    def get(self, request, *args, **kwargs):
        
        self._oauthsession.get_lists()
