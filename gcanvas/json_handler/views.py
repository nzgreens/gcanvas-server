import json
import logging
from datetime import datetime

#from django.shortcuts import get_object_or_404 #, render, redirect
from django.http import HttpResponse, Http404

from django.views.generic import ListView, View

from .models import Person, Address, UserPersonAssignment

class PeopleJsonView(ListView):
    model = Person

    template_name = "json_handler/people.json"
    context_object_name = 'people'

    
    def get(self, request, *args, **kwargs):
        #print(request)
        return super(PeopleJsonView, self).get(request, *args, **kwargs)


    def get_queryset(self):
        persons = [user_person_ass.person for user_person_ass in UserPersonAssignment.objects.filter(user=self.request.user)]
        return persons
    

    #All request will respond with content type of 'application/json'
    def render_to_response(self, context, **response_kwargs):
        response_kwargs.update({'content_type': 'application/json'})
        return super(PeopleJsonView, self).render_to_response(context, **response_kwargs)


    #update records
    def put(self, request, *args, **kwargs):
        people_map = json.loads(request.body.decode())
        for person_item in people_map['people']:
            try:
                person = Person.objects.select_related().get(external_id=person_item['id'])
                primary_address = person_item.get('primary_address', None)
                if primary_address is not None:
                    address, _ = Address.objects.select_related().get_or_create(
                        address1=primary_address.get('address1', person.primary_address.address1),
                        address2=primary_address.get('address2', person.primary_address.address2),
                        address3=primary_address.get('address3', person.primary_address.address3),
                        city=primary_address.get('city', person.primary_address.city),
                        state=primary_address.get('state', person.primary_address.state),
                        zip=primary_address.get('zip', person.primary_address.zip),
                        lat=primary_address.get('lat', person.primary_address.lat),
                        lng=primary_address.get('lng', person.primary_address.lng)
                    )
                else:
                    address = person.primary_address
                
                person.first_name=person_item.get('first_name', person.first_name)
                person.last_name=person_item.get('last_name', person.last_name)
                person.occupation=person_item.get('occupation', person.occupation)
                person.sex=person_item.get('sex', person.sex)
                person.birthdate=datetime.strptime(person_item.get('birthdate', '0001-01-01'), '%Y-%m-%d') if 'birthdate' in person_item.keys() else person.birthdate #could do it in get call, but this is simplier inmy eyes
                person.note=person_item.get('note', person.note)
                person.email=person_item.get('email', person.email)
                person.phone=person_item.get('phone', person.phone)
                person.primary_address=address
                person.contact_status_id=person_item.get('contact_status_id', person.contact_status_id)
                person.support_level=person_item.get('support_level', person.support_level)
                person.is_volunteer=person_item.get('is_volunteer', person.is_volunteer)
                person.host_billboard = person_item.get('host_billboard', person.host_billboard)
            
                person.save()
            except Exception as e:
                logging.error(e)
                raise e
                #@TODO: log something and return an error in JSON
                return HttpResponse('{"status": "error"}', content_type="application/json")
                

        return HttpResponse('{"status": "success"}')


    
    #create records
    def post(self, request, *args, **kwargs):
        people_map = json.loads(request.body.decode())
        for person_item in people_map['people']:
            try:
                #can be fetching the same address several times so using select_related
                #to stop the db from being called more than it's needed
                primary_address = person_item['primary_address']
                address, _ = Address.objects.select_related().get_or_create(
                    address1=primary_address.get('address1', ''),
                    address2=primary_address.get('address2', ''),
                    address3=primary_address.get('address3', ''),
                    city=primary_address.get('city', ''),
                    state=primary_address.get('state', ''),
                    zip=primary_address.get('zip', ''),
                    lat=primary_address.get('lat', 0.0),
                    lng=primary_address.get('lng', 0.0)
                )

                person, _ = Person.objects.select_related().get_or_create(
                    external_id=person_item['id'],
                    first_name=person_item['first_name'],
                    last_name=person_item['last_name'],
                    occupation=person_item.get('occupation', ''),
                    sex=person_item.get('sex', ''),
                    birthdate=datetime.strptime(person_item.get('birthdate', '0001-01-01'), '%Y-%m-%d'),
                    note=person_item.get('note', ''),
                    email=person_item.get('email', ''),
                    phone=person_item.get('phone', ''),
                    primary_address=address,
                    contact_status_id=person_item.get('contact_status_id'),
                    support_level=person_item.get('support_level'),
                    is_volunteer=person_item.get('is_volunteer', False)
                )
            except Exception as e:
                logging.error(e)
                return HttpResponse('{"status": "error"}', content_type="application/json")
                

        return HttpResponse('{"status": "success"}', content_type="application/json")



    #@KEEP: for reference purposes
    #from django.contrib.auth.decorators import login_required
    #from django.utils.decorators import method_decorator
    #@method_decorator(login_required)
    #def dispatch(self, *args, **kwargs):
    #    print("PeopleJsonView")
    #    print(args[0])
    #    print(kwargs)
    #    return super(PeopleJsonView, self).dispatch(*args, **kwargs)


class UserPeopleAssignment(View):
    def post(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass
    
