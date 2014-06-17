from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from .models import NationBuilderUser


class NationBuilderAuthBackend(ModelBackend):
    """Log in to Django using a NationBuilder user id

    """
    def authenticate(self, nation_user_id=None):
        try:
            return NationBuilderUser.objects.get(nation_user_id=nation_user_id).user
        except User.DoesNotExist:
            return None


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
