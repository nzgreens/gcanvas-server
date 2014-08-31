from django.shortcuts import render, redirect

from django.views.generic import View

from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from nationbuilder_connect.models import NationBuilderUser


class GCanvasUserView(View):
    #query status
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if NationBuilderUser.objects.filter(user=user).count():
                verified = True
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
            
        
        return HttpResponse('{"status": "unauthenticated"}',
                            content_type='application/json')


    
    def put(self, request, *args, **kwargs):
        return HttpResponse('{"status": "todo"}',
                            content_type='application/json')


    def post(self, request, *args, **kwargs):
        return HttpResponse('{"status": "todo"}',
                            content_type='application/json')


    def delete(self, request, *args, **kwargs):
        return HttpResponse('{"status": "todo"}',
                            content_type='application/json')



class GCanvasRegisterView(View):
    def get(self, request, *args, **kwargs):
        """
        Starts user down the registration path for NationBuilder
        """
        return redirect(reverse('app:main'))


    def post(self, request, *args, **kwargs):
        """
        Registers user locally giving an email and password
        """
        #@TODO: create a new user or set a password for it, setting that user as able to use password

        return redirect(reverse('app:main'))


class GCanvasLoginView(View):
    def get(self, request, *args, **kwargs):
        """
        Redirects user to login page
        """
        return redirect(reverse('app:main'))


    def post(self, request, *args, **kwargs):
        """
        Authenticate and login user
        """
        if 'email' in request.POST.keys() and 'password' in request.POST.keys():
            user = authenticate(request.POST['email'], request.POST['password'])
            if user != None:
                if NationBuilderUser.objects.filter(user=user).count():
                    verified = True
                else:
                    verified = False

                login(request, user)
                return HttpResponse(
                    '{"status": "authenticated", "verified": %s, "username": "%s", firstname": "%s", "lastname": "%s", "email": "%s"}' % 
                    (str(verified).lower(),
                     user.username,
                     user.first_name,
                     user.last_name,
                     user.email),
                    content_type='application/json')

        return HttpResponse('{"status": "unauthenticated"}',
                            content_type='application/json')
        
