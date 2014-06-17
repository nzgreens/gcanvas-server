import json

from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse, Http404



from .authenticator import OAuthSession, NationUserManager


class NationBuilderConnectView(View):
    def __init__(self, *args, **kwargs):
        super(NationBuilderConnectView, self).__init__(*args, **kwargs)
        client_id=settings.NATIONBUILDER_CLIENT_ID
        client_secret=settings.NATIONBUILDER_CLIENT_SECRET
        client_name=settings.NATIONBUILDER_CLIENT_NAME
        redirect_url="http://127.0.0.1:8000/nationbuilder/callback"
        self._oauthsession = OAuthSession(
            client_id,
            client_secret,
            client_name,
            redirect_url
        )

    def get(self, request, *args, **kwargs):
        if len(request.GET) > 0:
            if 'code' in request.GET:
                code = request.GET['code']
                token = self._oauthsession.get_access_token(code)
                print(token)
                nationmanager = NationUserManager()
                nationuser = nationmanager.create_nation_user(self._oauthsession, token)
                nationmanager.login(request, nationuser.nation_user_id)
                
                return HttpResponse("Success")
            else:
                return HttpResponse(json.dumps(request.GET), content_type='application/json')
        #token = 'fad163beeb0d92277a174c7b6979191d2f0d153fa9fae216e66e75418976d9ae'
        #api = '/api/v1/lists?per_page=100'
        #response = self._oauthsession.get_api_json_data(token, api)
        
        return redirect(self._oauthsession.get_authorisation_url()) #HttpResponse(response, content_type="application/json")
