from django.shortcuts import render, redirect

from django.views.generic import View

from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from email_verification.models import EmailVerified


class GCanvasUserView(View):
    #query status
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if EmailVerified.objects.filter(user=user).count():
                verified = EmailVerified.objects.get(user=user).verified
            else:
                verified = False

            return HttpResponse(
                '{"status": "authenticated", "verified": %s, "username": "%s", firstname": "%s", "lastname": "%s", "email": "%s"}' % 
                (str(verified).lower(),
                 user.username,
                 user.first_name, 
                 user.last_name, 
                 user.email),
                content_type='application/json')
            
        else:
            return HttpResponse('{"status": "unauthenticated"}',
                                content_type='application/json')


    #@TODO: Normal login to be done here
    #@TODO: Login via NationBuilders API http://nationbuilder.com/api_quickstart (I think that allows us to access a users Nation data via the API)
    #@TODO: store oauth_token, oauth_token_secret, and refresh_token for the user (or whatever the OAuth 2.0 calls for)
    def put(self, request, *args, **kwargs):
        return HttpResponse('{"status": "todo"}')


    def post(self, request, *args, **kwargs):
        return HttpResponse('{"status": "todo"}')


    def delete(self, request, *args, **kwargs):
        return HttpResponse('{"status": "todo"}')


class GCanvasLoginView(View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse('nationbuilder:connect'))
