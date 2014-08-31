import json

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from rauth import OAuth2Service

from .models import NationBuilderUser


def decode_json_byte_str(json_bytes):
    if isinstance(json_bytes, bytes):
        return json.loads(json_bytes.decode('utf-8'))
    else:
        return json.loads(json_bytes)


class OAuthSession(object):
    def __init__(
            self,
            client_id,
            client_secret,
            client_name,
            redirect_url,
            access_token_url='https://nzgreens.nationbuilder.com/oauth/token',
            authorise_url='https://nzgreens.nationbuilder.com/oauth/authorize',
            base_url='nzgreens.nationbuilder.com'
    ):
        self._base_url = base_url
        self._redirect_url = redirect_url
        
        self._service = OAuth2Service(
            client_id=client_id,
            client_secret=client_secret,
            name=client_name,
            authorize_url=authorise_url, #you'll note the correct spelling on the right hand side
            access_token_url=access_token_url,
            base_url=base_url
        )


    def get_authorisation_url(self):
        params = {'redirect_uri': self._redirect_url, 'response_type': 'code' } 
        return self._service.get_authorize_url(**params)


    def get_access_token(self, code):
        return self._service.get_access_token(decoder=decode_json_byte_str,
                                        data={"code": code,
                                              "redirect_uri": self._redirect_url,
                                              "grant_type": "authorization_code"}
        )


    
    #assumes api return JSON data
    def get_api_json_data(self, token, api, **kwargs):
        session = self._service.get_session(token)
        kwargs.update({'format': 'json'})
        return session.get("https://%s%s" % (self._base_url, api),
                           params=kwargs,
                           headers={'content-type': 'application/json'}).json()


    def whoami(self, token):
        return self.get_api_json_data(token, '/api/v1/people/me')



    def get_lists(self, token):
        result = self.get_api_json_data(token, '/api/v1/lists', {'per_page': 100})
        pages = [result]
        while 'page' in result and int(result['page']) < int(result['total_pages']):
            page = int(result['page'])
            result = self.get_api_json_data(token, '/api/v1/lists', {'page': page+1, 'per_page': 100})
            pages.append(result)

        return [result for page in pages for result in page['results']]
    

class NationUserManager(object):
    def create_nation_user(self, oauthsession, oauth_token):
        profile_json = oauthsession.whoami(oauth_token)
        nation_id = profile_json['person']['id']
        email = profile_json['person']['email']
        firstname = profile_json['person']['first_name']
        lastname = profile_json['person']['last_name']
        username = '%s%s%d' % (firstname, lastname, nation_id)
        username = username.lower()
        if User.objects.filter(username=username).count():
            user = User.objects.get(username=username)
        else:
            #alright, they have verified themselves on NationBuilder, but no user has been created this end
            #not sure how this happened, so we'll just create a new user and wait for them to give it a password
            #@TOTO: autogenerate a password, and email it to the user using the email gained from NationBuilder.
            user = User.objects.create_user(username, email, '')
            #however for the moment, we just make sure the account can't be used till a password has been set
            #thus stopping others from using this id unauthorised
            user.set_unusable_password()

        user.first_name = firstname
        user.last_name = lastname
        user.email = email
        user.save()

        nationuser, _ = NationBuilderUser.objects.get_or_create(nation_user_id=nation_id, user=user)
        nationuser.oauth_token = oauth_token
        nationuser.save()

        return nationuser


    def is_nation_user(self, user):
        return User.objects.filter(username=username).count() > 0


    def get_nation_user(self, user):
        return NationBuilderUser.objects.get(user=user)


    def login(self, request, nation_id):
        user = authenticate(nation_user_id=nation_id)
        if user != None:
            login(request, user)

        return user != None


    def logout(self, request):
        logout(request)
        
