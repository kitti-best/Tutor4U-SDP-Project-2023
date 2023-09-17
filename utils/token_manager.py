from rest_framework_simplejwt.tokens import RefreshToken
from KMITLWebAppClassProject.settings import SIMPLE_JWT
from datetime import datetime
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import jwt

import environ
env = environ.Env()
environ.Env.read_env()

class TokenManager:

    def _validate(task):
        def wrapper(input):
            if (input is None):
                raise ValueError('\'input\' cannot be NoneType')
            return task(input)
        return wrapper
    
    @staticmethod
    @_validate
    def generate(user):
        token = RefreshToken.for_user(user)
        return (str(token.access_token).encode('utf-8'), str(token).encode('utf-8'))
    
    @staticmethod
    @_validate
    def extract(input_token):
        token = jwt.decode(
                    input_token, 
                    key=SIMPLE_JWT.get('SIGNING_KEY'), 
                    algorithm=SIMPLE_JWT.get('ALGORITHM')
                )
        
        expire_date = token.get('expire_date', None)
        date_now = int(datetime.utcnow().timestamp())
        if (date_now >= expire_date):
            return None

        return token