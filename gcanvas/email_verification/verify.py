from django.contrib.auth.models import User
from django.core.mail import send_mail
from mailgun_validation.validators import validate_email

from .models import EmailVerified

class Verifier(object):
    def __init__(self):
        pass

    def validate(self, email):
        try:
            validate_email(email)

            return True
        except:
            return False

    def send_verification_code(self, username, to_email, verfication_url, from_email='james.hurford@greens.org.nz'):
        message = """
        Hi %s

        Thank you for registering.  Please visit the link below, to verify your email address.

        %s

        Thank you
        gCanvas Team
        """ % (username, verfication_url)

        try:
            send_email("gCanvas Email verification", message, from_email, [to_email], fail_silently=False)
        except:
            return False

        return True
            
        

    def verify(self, code, original):
        return code == original
