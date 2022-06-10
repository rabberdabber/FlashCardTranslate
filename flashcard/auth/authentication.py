''' Reference:
https://auth0.com/docs/quickstart/backend/python'''


import json
from functools import wraps
from urllib.request import urlopen

from flask import render_template, request,session,abort
from jose import jwt

import sys
sys.path.append('../../')
from config import Config

ALGORITHMS = ['RS256']
AUTH0_DOMAIN = Config.AUTH0_DOMAIN
AUTH0_AUDIENCE = Config.AUTH0_AUDIENCE
AUTH0_CLIENTID = Config.AUTH0_CLIENTID


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    # sourcery skip: inline-immediately-returned-variable
    '''Obtains Access Token from the Authorization Header'''
    auth = request.headers.get('Authorization', None)
    if auth is None:
        raise AuthError(
            {
                'code': 'authorization_header_missing',
                'description': 'Authorization header is expected',
            },
            401,
        )

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise AuthError(
            {
                'code': 'invalid_header',
                'description': 'Authorization header must start with' ' Bearer',
            },
            401,
        )
    elif len(parts) == 1:
        raise AuthError(
            {'code': 'invalid_header', 'description': 'Token not found'}, 401
        )
    elif len(parts) > 2:
        raise AuthError(
            {
                'code': 'invalid_header',
                'description': 'Authorization header must be' ' Bearer token',
            },
            401,
        )

    token = parts[1]
    return token


def verify_decode_jwt(token):  # sourcery skip: raise-from-previous-error
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError(
            {'code': 'invalid_header', 'description': 'Authorization malformed.'}, 401
        )

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e'],
            }
    if rsa_key:
        try:
            # return payload
            return jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=AUTH0_CLIENTID,
                issuer=f'https://{AUTH0_DOMAIN}/',
            )

        except jwt.ExpiredSignatureError:
            raise AuthError(
                {'code': 'token_expired', 'description': 'Token expired.'}, 401
            )

        except jwt.JWTClaimsError:
            raise AuthError(
                {
                    'code': 'invalid_claims',
                    'description': 'Incorrect claims. Please, check the audience and issuer.',
                },
                401,
            )
        except Exception:
            raise AuthError(
                {
                    'code': 'invalid_header',
                    'description': 'Unable to parse authentication token.',
                },
                400,
            )
    raise AuthError(
        {
            'code': 'invalid_header',
            'description': 'Unable to find the appropriate key.',
        },
        400,
    )



def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):  # sourcery skip: raise-from-previous-error
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            if 'sub' not in session:
                session['sub'] = payload['sub']
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator

def requires_login():
    def requires_login_decorator(f):
        @wraps(f)
        def wrapper(*args,**kwargs):
            if 'sub' not in session:
                return abort(401)
                
            return f(*args,**kwargs)
        return wrapper
    return requires_login_decorator