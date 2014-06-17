import json
from urllib.parse import parse_qs

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.conf import settings
from django.http import HttpResponse, Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from requests_oauthlib import OAuth1Session
#import requests
#from requests_oauthlib import OAuth1

from .models import TwitterUser, UserResources

class Authenticate(object):
    def __init__(
            self,
            client_id,
            client_secret,
            request_token_url='https://api.twitter.com/oauth/request_token',
            base_authorization_url='https://api.twitter.com/oauth/authenticate',
            access_token_url = 'https://api.twitter.com/oauth/access_token',
            verify_url='https://api.twitter.com/1.1/account/verify_credentials.json'):

        #'http://localhost:8000/twitter',
        self._client_id = client_id
        self._client_secret = client_secret
        self._request_token_url = request_token_url
        self._base_authorization_url = base_authorization_url
        self._access_token_url = access_token_url
        self._verify_url = verify_url
        self._oauth = None
                


    def get_request_tokens(self):
        oauth = OAuth1Session(self._client_id,
                              client_secret=self._client_secret)
                              
        resource = oauth.fetch_request_token(self._request_token_url)
        resource = {isinstance(key, bytes) and key.decode('utf-8') or key: isinstance(resource[key], bytes) and resource[key].decode('utf-8') or resource[key] for key in resource}
        UserResources.objects.get_or_create(owner_key=resource.get('oauth_token'), owner_secret=resource.get('oauth_token_secret'))

        return resource, oauth.authorization_url(self._base_authorization_url)
        

    def get_authorisation_url(self, oauth_token):
        try:
            user_resource = UserResources.objects.get(owner_key=oauth_token)
        except:
            return "/"
        else:
            oauth = OAuth1Session(self._client_id, 
                                  client_secret=self._client_secret,
                                  resource_owner_key=user_resource.owner_key,
                                  resource_owner_secret=user_resource.owner_secret)
            return oauth.authorization_url(self._base_authorization_url)

        
        
        

    def get_access_token(self, oauth_token, verifier):
        try:
            user_resource = UserResources.objects.get(owner_key=oauth_token)
        except:
            return {'oauth_token': '', 'oauth_token_secret': ''}
        else:            
            oauth = OAuth1Session(self._client_id,
                                  client_secret=self._client_secret,
                                  resource_owner_key=user_resource.owner_key,
                                  resource_owner_secret=user_resource.owner_secret,
                                  verifier=verifier)
            resource = oauth.fetch_access_token(self._access_token_url)
            resource = {isinstance(key, bytes) and key.decode('utf-8') or key: isinstance(resource[key], bytes) and resource[key].decode('utf-8') or resource[key] for key in resource}

            
            return resource


    def create_twitter_user(self, twitter_id, screen_name, oauth_token, oauth_token_secret):
        if User.objects.filter(username=screen_name).count():
            user = User.objects.get(username=screen_name)
        else:
            user = User.objects.create_user(screen_name, '', '')
        user.set_unusable_password()
        #make sure only one is created for each user, so if already there won't create a new one'
        twitter_user, _ = TwitterUser.objects.get_or_create(
            user=user,
            twitter_id=twitter_id,
            twitter_screen_name=screen_name,
            oauth_token_secret=oauth_token_secret,
            oauth_token=oauth_token
        )
        
        return twitter_user


    def verify_credentials(self, twitter_id):
        twitter_user = TwitterUser.objects.get(twitter_id=twitter_id)
        oauth = OAuth1Session(self._client_id,
                              client_secret=self._client_secret,
                              resource_owner_key=twitter_user.oauth_token,
                              resource_owner_secret=twitter_user.oauth_token_secret)
        response = oauth.get(self._verify_url)

        return response.status_code == 200 and response.json()['id_str'] == twitter_user.twitter_id
        

class TwitterAuthView(View):
    def __init__(self, *args, **kwargs):
        super(TwitterAuthView, self).__init__(*args, **kwargs)
        
        self._authenticate = Authenticate(settings.TWITTER_CLIENT_ID, settings.TWITTER_CLIENT_SECRET)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return self._redirect_to_registration()

        if len(request.GET) > 0:
            access_tokens = self._authenticate.get_access_token(request.GET['oauth_token'], request.GET['oauth_verifier'])
            self._authenticate.create_twitter_user(access_tokens['user_id'], access_tokens['screen_name'], access_tokens['oauth_token'], access_tokens['oauth_token_secret'])
            
            if self._authenticate.verify_credentials(access_tokens['user_id']):
                user = authenticate(twitter_id=access_tokens['user_id'])
                if user != None:
                    login(request, user)
                else:
                    raise PermissionDenied

                return self._redirect_to_registration()
            
            else:
                raise PermissionDenied

        resource, authorisation_url = self._authenticate.get_request_tokens()
        
        return redirect(authorisation_url, permanent=True)


    def post(self, request, *args, **kwargs):
        print(request.POST)

        return HttpResponse('{"oauth_token":"hello"}', content_type="application/json")
        

    def _redirect_to_registration(self):
        if hasattr(settings, 'USER_REGISTER_URL'):
            return redirect(settings.USER_REGISTER_URL)
        else:
            return HttpResponse("Please add USER_REGISTER_URL to the settings file")
