from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import View

from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404

from django.core.mail import send_mail

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.http import QueryDict
from  django.db.utils import IntegrityError

from .models import *

import os
import json
import datetime
import logging

class GCanvasUserView(View):
    #query status
    def get(self, request, *args, **kwargs):
        logging.error("user.json")
        if request.user.is_authenticated() and request.user.validated == True:
            verified = request.user.validated
            jsonStr = '{"status": "authenticated", "verified": %s, "username": "%s", "firstname": "%s", "lastname": "%s", "email": "%s"}' % (str(verified).lower(), str(request.user.username), request.user.firstname, request.user.lastname, request.user.email)
                
            return HttpResponse(
                jsonStr,
                content_type='application/json')


        token = get_token(request)
        
        response = HttpResponse('{"status": "unauthenticated", "token": "%s"}' %(token),
                                content_type='application/json')

        response.set_cookie('csrftoken', token)

        return response


    
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
  def post(self, request, *args, **kwargs):
        """
        Registers user locally giving an email and password
        """
        #@TODO: create a new user or set a password for it, setting that user as able to use password

        data = json.loads(request.read().decode());
        logging.error(data)
        try:
          user = get_user_model().objects.create_user(data['username'], data['firstname'], data['lastname'], data['email'], password=data['password'])
          verify_code, _ = GCanvasUserVerification.objects.get_or_create(user=user)
          
          verify_url = reverse("accounts:verification", args=(verify_code.code.hex,))
          message = """
          Hi %s

          Thank you for registering.  Please visit the link below, to verify your email address.

          %s

          Thank you
          gCanvas Team
          """ % (user.username, verify_url)

          from_email='terraundersea@gmail.com'
          result = send_mail("gCanvas Email verification", message, from_email, [user.email], fail_silently=False)
        except IntegrityError as e:
          return HttpResponse('{"status": "duplicate", "duplicates": ["username"]}',
                            content_type='application/json')
        except ValueError as e:
          return HttpResponse('{"status": "missing-data"}',
                            content_type='application/json')
        except KeyError as e:
          return HttpResponse('{"status": "missing-keys", "missing": "%(missing)s"}' % {'missing': str(e).replace("'", "")},
                            content_type='application/json')
        except Exception as e:
          logging.error("An error occured when registering a new user: %(message)s" % {'message': str(e)})
          return HttpResponse('{"status": "error", "message": "An error has occured.  Sorry for the inconvenience"}',
                            content_type='application/json')

        
        return HttpResponse('{"status": "registered"}',
                          content_type='application/json')


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
        data = json.loads(request.read().decode())
        logging.error(data)
        if 'username' in data.keys() and 'password' in data.keys():
            user = authenticate(username=data['username'], password=data['password'])
            if user != None and user.validated:
              login(request, user)
              return HttpResponse(
                    '{"status": "authenticated", "validated": %s, "username": "%s", "firstname": "%s", "lastname": "%s", "email": "%s"}' % 
                    (str(user.validated).lower(),
                     user.username,
                     user.firstname,
                     user.lastname,
                     user.email),
                    content_type='application/json')

        return HttpResponse('{"status": "unauthenticated"}',
                            content_type='application/json')
        


class GCanvasVerificationView(View):
  def get(self, request, code, *args, **kwargs):
    user_verification = get_object_or_404(GCanvasUserVerification, code=code)

    user_verification.user.validated = True
    user_verification.user.save()

    user_verification.delete()
    

    return redirect(reverse('app:main'))
