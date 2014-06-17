import json
from datetime import datetime

#from django.shortcuts import get_object_or_404 #, render, redirect
from django.http import HttpResponse, Http404

from django.views.generic import ListView

from .models import People, Address

class PeopleJsonView(ListView):
    model = People

    template_name = "json_handler/people.json"
    context_object_name = 'people'

    
    def get(self, request, *args, **kwargs):
        #print(request)
        return super(PeopleJsonView, self).get(request, *args, **kwargs)


    #All request will respond with content type of 'application/json'
    def render_to_response(self, context, **response_kwargs):
        response_kwargs.update({'content_type': 'application/json'})
        return super(PeopleJsonView, self).render_to_response(context, **response_kwargs)


    #update records
    def put(self, request, *args, **kwargs):
        people_map = json.loads(request.body)
        for person_item in people_map['people']:
            try:
                person = People.objects.get(nation_id=person_item['id'])
                person.note = person_item['note']
                person.email = person_item['email']
                person.phone = person_item['phone']
                person.contact_status_id = person_item['contact_status_id']
                person.support_level = person_item['support_level']
                person.is_volunteer = person_item['is_volunteer']
                person.host_billboard = person_item['host_billboard']
                person.save()
            except:
                #@TODO: log something and return an error in JSON
                return HttpResponse('{"status": "success"}', content_type="application/json")
                

        return HttpResponse('{"status": "success"}')


    
    #create records
    def post(self, request, *args, **kwargs):
        people_map = json.loads(request.body)
        for person_item in people_map['people']:

            #can be fetching the same address several times so using select_related
            #to stop the db from being called more than it's needed
            address = Address.objects.select_related().get_or_create(
                address1=person_item['primary_address']['address1'],
                address2=person_item['primary_address']['address2'],
                address3=person_item['primary_address']['address3'],
                city=person_item['primary_address']['city'],
                state=person_item['primary_address']['state'],
                zip=person_item['primary_address']['zip'],
                lat=person_item['primary_address']['lat'],
                lng=person_item['primary_address']['lng'],
            )

            person = People.objects.get_or_create(
                nation_id=person_item['id'],
                first_name=person_item['first_name'],
                last_name=person_item['last_name'],
                occupation=person_item['occupation'],
                sex=person_item['sex'],
                birthdate=datetime.strptime(person_item['birthdate'], '%Y-%m-%d'),
                note=person_item['note'],
                email=person_item['email'],
                phone=person_item['phone'],
                primary_address=address,
                contact_status_id=person_item['contact_status_id'],
                support_level=person_item['support_level'],
                is_volunteer=person_item['is_volunteer']
            )

        return HttpRespnose('{"status": "success"}', content_type="application/json")



    #@KEEP: for reference purposes
    #from django.contrib.auth.decorators import login_required
    #from django.utils.decorators import method_decorator
    #@method_decorator(login_required)
    #def dispatch(self, *args, **kwargs):
    #    print("PeopleJsonView")
    #    print(args[0])
    #    print(kwargs)
    #    return super(PeopleJsonView, self).dispatch(*args, **kwargs)
