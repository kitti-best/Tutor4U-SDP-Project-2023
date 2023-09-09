import environ
from datetime import datetime, timedelta
import jwt

env = environ.Env()
environ.Env.read_env()

class TokenManager:

    @staticmethod
    def build(username, option=None):
        if (option is None):
            raise ValueError('\'option\' cannot be NoneType')
        
        if (option in ['ACCESS', 'REFRESH']):
            option += '_SECRET'
            days = 1
            if (option == 'REFRESH'):
                days = 7
        else:
            raise ValueError('\'option\' must be \'ACCESS\ or \'REFRESH\'')
        
        return TokenManager.generate(username, env(option), days)

    @staticmethod
    def generate(username, secret_key, days):
        date_now = datetime.utcnow()
        payload = {
            'username': username, 
            'expire_in': f'{date_now + timedelta(days=days)}', 
            'iat': f'{date_now}'
        }
        
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token