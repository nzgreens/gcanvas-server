from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from .models import TwitterUser


class TwitterAuthBackend(ModelBackend):
    """Log in to Django using a twitter id

    """
    def authenticate(self, twitter_id):
        try:
            return TwitterUser.objects.get(twitter_id=twitter_id).user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
