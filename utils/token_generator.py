import environ
from datetime import datetime, timedelta
import jwt

env = environ.Env()
environ.Env.read_env()

class TokenManager:

    def _validate(task):
        def wrapper(username, option=None):
            if (option is None):
                raise ValueError('\'option\' cannot be NoneType')
            
            if (option in ['ACCESS', 'REFRESH']):
                option += '_SECRET'
                days = 1
                if (option == 'REFRESH'):
                    days = 7
            else:
                raise ValueError('\'option\' must be \'ACCESS\ or \'REFRESH\'')
            return task(username, env(option), days)
        return wrapper
    
    @staticmethod
    @_validate
    def generate(username, secret_key, days):
        date_now = datetime.utcnow()
        payload = {
            'username': username, 
            'expire_date': int((date_now + timedelta(days=days)).timestamp()), 
        }
        
        token = jwt.encode(payload, secret_key, algorithm='HS256').decode('utf-8')
        return token
    
    @staticmethod
    @_validate
    def extract(input_token, secret_key, days):
        token = jwt.decode(input_token, secret_key, algorithm='HS256')
        expire_date = token.get('expire_date', None)
        
        date_now = int(datetime.utcnow().timestamp())
        if (date_now >= expire_date):
            return None
        
        return token