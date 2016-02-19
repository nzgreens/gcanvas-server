import json
import datetime
import os

from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings
from django.utils.http import urlencode, urlquote
from django.core.mail import send_mail, outbox

from gcanvas_user.models import GCanvasUser, GCanvasUserManager, GCanvasUserVerification
from json_handler.models import Address, Person, UserPersonAssignment
from django.contrib.auth import get_user_model


def loadPeople():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    with open('%(scriptdir)s/testdata/people.json' % {'scriptdir': script_dir}) as p:
        return json.load(p)


def parsePeople(people):
    for person in people['results']:
        createPerson(person)
        
def createAddress(address):
    address = {x:address[x] for x in address if address[x] is not None}
    address, _ = Address.objects.get_or_create(address1=address.get('address1', ''),
                                            address2=address.get('address2', ''),
                                            address3=address.get('address3', ''),
                                            city=address.get('city', ''),
                                            state=address.get('state', ''),
                                            zip=address.get('zip', ''),
                                            lat=address.get('lat', 0.0),
                                            lng=address.get('lng', 0.0))


    return address


def createPerson(person):
    address = createAddress(person['primary_address'])
    birthdate = datetime.datetime.strptime(person.get('birthdate', '0000-00-00'), '%Y-%m-%d')
    person, _ = Person.objects.get_or_create(external_id=person['id'],
                                             first_name=person.get('first_name', ''),
                                             last_name=person.get('last_name', ''),
                                             occupation=person.get('occupation', ''),
                                             sex=person.get('sex', ''),
                                             birthdate=birthdate,
                                             note=person.get('note', ''),
                                             email=person.get('email', ''),
                                             phone=person.get('phone', ''),
                                             primary_address=address,
                                             support_level=person.get('support_level', None),
                                             is_volunteer=person.get('is_volunteer', False))

                                 


def assignPeopleToUser(user, people):
    for person in people:
        UserPersonAssignment.objects.get_or_create(user=user, person=person)

class GCanvasUserTests(TestCase):
    @override_settings(AUTH_USER_MODEL='gcanvas_user.GCanvasUser')
    def setUp(self):
        model = get_user_model()
        user1 = model.objects.create_user("testuser", firstname="test", lastname="user", email="testuser@gcanvasuser", password="password")
        user1.validated = True
        #user1.set_password("password")
        self.user2 = model.objects.create_user(username="testuser2", firstname="test2", lastname="user2", email="testuser2@gcanvasuser", password="password2")
        #user2.set_password("password2")
        self.user2.validated=True
        self.user2.save()

        
        self.login_user_url = reverse("accounts:login")
        
        post = json.dumps({"username": "testuser2", "password": "password2"})

        response = self.client.post(self.login_user_url, post, "application/json")

        data = response.content.decode()

        self.people = loadPeople()
        parsePeople(self.people)

        

    def test_addresses_are_present(self):
        addresses = Address.objects.all();

        self.assertEquals(len(addresses), 2)



    def test_people_are_present(self):
        people = Person.objects.all()

        self.assertEqual(len(people), 3)
        
    def test_user_can_only_download_people_assigned_to_them(self):
        people = Person.objects.all()
        assignPeopleToUser(self.user2, people[:2])
        
        people_url = reverse('json:people_json')

        people_json = self.client.get(people_url).content.decode()

        data = json.loads(people_json)

        self.assertTrue('results' in data.keys())
        self.assertEquals(len(data['results']), 2)


    def test_upload_people(self):
        post = json.dumps({'people': [
            {
                "birthdate": "1973-04-04",
                "email": "festeban@example.com",
                "first_name": "Fernando",
                "id": 500,
                "is_volunteer": False,
                "last_name": "Esteban",
                "note": "Has 3 kids. Ask about the baby on the way",
                "occupation": "Community Organizer",
                "phone": "2156726335",
                "primary_address": {
                    "address1": "448 S Hill St",
                    "address2": "Suite 200",
                    "address3": None,
                    "city": "Los Angeles",
                    "state": "CA",
                    "country_code": "US",
                    "zip": "90013",
                    "lat": 34.0502,
                    "lng": -117.2478
                },
                "sex": "F",
                "support_level": 1,
                
            },
        ]})

        create_url = reverse('json:people_json')

        response = self.client.post(create_url, post, "application/json")

        data = response.content.decode()
        data = json.loads(data)

        content = {"status": "success"}

        self.assertEquals(data, content)

        person = Person.objects.get(external_id=500)

        self.assertIsNotNone(person)


    def test_modify_person_details(self):
        createPerson({
                "birthdate": "1973-04-04",
                "email": "festeban@example.com",
                "first_name": "Fernando",
                "id": 500,
                "is_volunteer": False,
                "last_name": "Esteban",
                "note": "Has 3 kids. Ask about the baby on the way",
                "occupation": "Community Organizer",
                "phone": "2156726335",
                "primary_address": {
                    "address1": "448 S Hill St",
                    "address2": "Suite 200",
                    "address3": None,
                    "city": "Los Angeles",
                    "state": "CA",
                    "country_code": "US",
                    "zip": "90013",
                    "lat": 34.0502,
                    "lng": -117.2478
                },
                "sex": "F",
                "support_level": 1,
                
            })
        person_orig = Person.objects.get(external_id=500)
        modify_url = reverse('json:people_json')
        put = json.dumps({'people': [
            {
                "birthdate": "1973-04-04",
                "email": "festeban@example.com",
                "first_name": "Jim",
                "id": 500,
                "is_volunteer": True,
                "last_name": "Hurford",
                "note": "Has 3 kids. Ask about the baby on the way",
                "occupation": "Community Organizer",
                "phone": "2156726335",
                "primary_address": {
                    "address1": "448 S Hill St",
                    "address2": "Suite 200",
                    "address3": None,
                    "city": "Los Angeles",
                    "state": "CA",
                    "country_code": "US",
                    "zip": "90013",
                    "lat": 34.0502,
                    "lng": -117.2478
                },
                "sex": "F",
                "support_level": 1,
                
            },
        ]})
        
        response = self.client.put(modify_url, put, "application/json")

        data = response.content.decode()
        data = json.loads(data)

        content = {"status": "success"}

        self.assertEquals(data, content)

        person_modified = Person.objects.get(external_id=500)

        self.assertIsNotNone(person_modified)
