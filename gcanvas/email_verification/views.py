import uuid
import json

from django.shortcuts import render

from django.views.generic import View

#from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404

from .models import EmailVerified

from .verify import Verifier

#TODO: create a view to recieve a code sent by email to verify email has been recieved
#this is a REST server
class EmailVerifierRESTView(View):
    def __init__(self, *args, **kwargs):
        self._verifier = Verifier()
        
        super().__init__(*args, **kwargs)

    #request email verification
    def post(self, request, *args, **kwargs):
        verify_object = EmailVerified.objects.get_or_create(user=request.user, code=str(uuid.uuid1()))
        if verify_object.valid == True and self._verifier.validate(request.user.email):
            name = "%s %s" % (request.user.firstname, request.user.lastname)
            verfication_url = request.build_absolute_uri('#%s' % (verify_object.code))
            self._validate.send_verification_code(self, name, request.user.email, verfication_url) 
        elif verify_object.valid == True:
            verify_object.valid = False
            verify_object.save()

            return HttpResponse('{"status": "failure", "message": "The email provided is invalid"}', content_type="application/json")

        return HttpResponse('{"status": "posted"}', content_type="application/json")

    
    #verify with verification code
    def put(self, request, *args, **kwargs):
        code_map = json.loads(request.body)
        if 'code' in code_map.keys():
            code = code_map['code']
            try:
                verify_object = EmailVerified.objects.get(code=code)
                verify_object.verified = True
                emailverify.save()
            except:
                return HttpResponse('{"status": "unverified", "message": "code did not match"}', content_type="application/json")

        return HttpResponse('{"status": "verified"}', content_type="application/json")


    #return verification status
    def get(self, request, *args, **kwargs):
        if 'email' in request.GET.keys():
            email = request.GET['email']
            try:
                user = User.objects.get(email=email)
            except:
                raise Http404
            else:
                try:
                    verify_object = EmailVerified.objects.get(user=user)
                    if verify_object.verified == False:
                        return HttpResponse('{"status": "unverified"}', content_type="application/json")
                except:
                    return HttpResponse('{"status": "unverified"}', content_type="application/json")

        return HttpResponse('{"status": "verified"}', content_type="application/json")


