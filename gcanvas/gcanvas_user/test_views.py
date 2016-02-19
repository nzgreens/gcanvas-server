import json

from django.test.utils import setup_test_environment
from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings
from django.utils.http import urlencode, urlquote
from django.core.mail import send_mail, outbox

import django.core.mail as mail

from gcanvas_user.models import GCanvasUser, GCanvasUserManager, GCanvasUserVerification
from django.contrib.auth import get_user_model

class GCanvasUserTests(TestCase):
    @override_settings(AUTH_USER_MODEL='gcanvas_user.GCanvasUser')
    def setUp(self):
        setup_test_environment()
        model = get_user_model()
        user1 = model.objects.create_user("testuser", firstname="test", lastname="user", email="testuser@gcanvasuser", password="password")
        user1.validated = False
        #user1.set_password("password")
        user2 = model.objects.create_user(username="testuser2", firstname="test2", lastname="user2", email="testuser2@gcanvasuser", password="password2")
        #user2.set_password("password2")
        user2.validated=True
        user2.save()

        verify_code, _ = GCanvasUserVerification.objects.get_or_create(user=user1)

        self.status_user_url = reverse("accounts:user")
        self.register_user_url = reverse("accounts:register")
        self.login_user_url = reverse("accounts:login")
        self.verify_user_url = reverse("accounts:verification", args=(verify_code.code.hex,))



    def test_initial_status_should_be_unauthorised_and_includes_token(self):
        response = self.client.get(self.status_user_url)

        data = response.content.decode()
        data = json.loads(data)
        #{"status": "unauthenticated", "token": "%s"}' %(token

        self.assertEquals(data['status'], "unauthenticated")
        self.assertTrue("token" in data.keys())



    def test_login_with_validated_user_should_succeed(self):
        post = json.dumps({"username": "testuser2", "password": "password2"})

        response = self.client.post(self.login_user_url, post, "application/json")

        data = response.content.decode()
        data = json.loads(data)

        content = {"status": "authenticated", "validated": True, "username": "testuser2", "firstname": "test2", "lastname": "user2", "email": "testuser2@gcanvasuser"}

        self.assertEquals(data, content)




    def test_login_with_unvalidated_user_should_fail(self):
        post = json.dumps({"username": "testuser", "password": "password"})

        response = self.client.post(self.login_user_url, post, "application/json")

        data = response.content.decode()
        data = json.loads(data)

        content = {"status": "unauthenticated"}

        self.assertEquals(data, content)


    def test_register_user_should_return_status_registered(self):
        post = json.dumps({"username": "testuser3", "firstname": "test3", "lastname": "user3", "email": "testuser3@gcanvasuser", "password": "password3"})

        response = self.client.post(self.register_user_url, post, "application/json")

        data = response.content.decode()
        data = json.loads(data)

        content = {"status": "registered"}

        self.assertEquals(data, content)


    def test_register_user_with_already_used_username_should_return_status_duplicate_and_what_is_duplicated(self):
        post = json.dumps({"username": "testuser2", "firstname": "test2", "lastname": "user2", "email": "testuser2@gcanvasuser", "password": "password2"})

        response = self.client.post(self.register_user_url, post, "application/json")

        data = response.content.decode()
        data = json.loads(data)

        content = {"status": "duplicate", "duplicates": ["username"]}

        self.assertEquals(data, content)


    def test_register_user_with_missing_firstname_should_return_status_missing_keys_with_missing_being_firstname(self):
        post = json.dumps({"username": "username4", "lastname": "user2", "email": "testuser2@gcanvasuser", "password": "password2"})

        response = self.client.post(self.register_user_url, post, "application/json")

        data = response.content.decode()
        data = json.loads(data)

        content = {"status": "missing-keys", "missing": "firstname"}

        self.assertEquals(data, content)



    def test_register_user_with_missing_username_should_return_status_missing_keys_with_missing_being_username(self):
        post = json.dumps({"firstname": "test4", "lastname": "user2", "email": "testuser2@gcanvasuser", "password": "password2"})

        response = self.client.post(self.register_user_url, post, "application/json")

        data = response.content.decode()
        data = json.loads(data)

        content = {"status": "missing-keys", "missing": "username"}

        self.assertEquals(data, content)




    def test_register_user_with_missing_lastname_should_return_status_missing_keys_with_missing_being_lastname(self):
        post = json.dumps({"username": "username4", "firstname": "user2", "email": "testuser2@gcanvasuser", "password": "password2"})

        response = self.client.post(self.register_user_url, post, "application/json")

        data = response.content.decode()
        data = json.loads(data)

        content = {"status": "missing-keys", "missing": "lastname"}

        self.assertEquals(data, content)




    def test_register_user_with_missing_email_should_return_status_missing_keys_with_missing_being_email(self):
        post = json.dumps({"username": "username4", "firstname": "user2", "lastname": "user2", "password": "password2"})

        response = self.client.post(self.register_user_url, post, "application/json")

        data = response.content.decode()
        data = json.loads(data)

        content = {"status": "missing-keys", "missing": "email"}

        self.assertEquals(data, content)




    def test_register_user_with_missing_password_should_return_status_missing_keys_with_missing_being_password(self):
        post = json.dumps({"username": "username4", "firstname": "user2", "lastname": "user2", "email": "testuser2@gcanvasuser"})

        response = self.client.post(self.register_user_url, post, "application/json")

        data = response.content.decode()
        data = json.loads(data)

        content = {"status": "missing-keys", "missing": "password"}

        self.assertEquals(data, content)



    def test_verifcation_of_user(self):
        self.client.get(self.verify_user_url)

        post = json.dumps({"username": "testuser", "password": "password"})

        response = self.client.post(self.login_user_url, post, "application/json")

        data = response.content.decode()
        data = json.loads(data)

        content = {"status": "authenticated", "validated": True, "username": "testuser", "firstname": "test", "lastname": "user", "email": "testuser@gcanvasuser"}

        self.assertEquals(data, content)



    def test_registering_user_sends_email(self):
        post = json.dumps({"username": "username5", "firstname": "user2", "lastname": "user2", "email": "testuser5@gcanvasuser", "password": "pass"})

        self.client.post(self.register_user_url, post, "application/json")

        user5 = get_user_model().objects.get(username='username5')
        user_verification = GCanvasUserVerification.objects.get(user=user5)

        verify_user_url = reverse("accounts:verification", args=(user_verification.code.hex,))

        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, "gCanvas Email verification")
        self.assertEquals(mail.outbox[0].to, ["testuser5@gcanvasuser"])
        self.assertTrue(mail.outbox[0].message().as_string().find(verify_user_url) > 0)
