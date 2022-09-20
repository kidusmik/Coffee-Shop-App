import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

from settings import ALGORITHMS, API_AUDIENCE, AUTH0_DOMAIN

# AuthError Exception


class AuthError(Exception):
    """Defines a class AuthError Exception, A standardized way to communicate
    auth failure modes.

    Attributes:
        error (dict): Contains error information such as code and description
        status_code (int): HTTP error status code

    Arguments:
        error (dict): The error information
        status_code (int): The HTTP error status code
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

# Most of this code is taken from Udacity class notes and exercises
def get_token_auth_header():
    """
    Attemps to get the header from the request, splits the header into bearer
    and token to get the token.

    Arguments:
        None

    Returns:
        - token (str): The token that is fetched by splitting the header.

    Raises:
        - AuthError (401):
            - If authorization header is missing
            - If the token is not a bearer token or if the token is not found.
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


# Most of this code is taken from Udacity class notes and exercises
def check_permissions(permission, payload):
    """
    Checks if the payload includes the permission that is needed.

    Arguments:
        permission (str): The Auth0 RBAC permission
        payload (str): the JWT token

    Returns:
        - True on success

    Raises:
        - AuthError (400): If the permissions list is not found in the payloadd
        - AuthError (403): If the permission is not found
    """
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True


# Most of this code is taken from Udacity class notes and exercises
def verify_decode_jwt(token):
    """
    Checks if the token is an Auth0 token with key id (kid), verifies
    the token using Auth0 /.well-known/jwks.json, decodes the payload
    from the token and validates the claims.

    Arguments:
        token (str): The JWT token

    Returns:
        - payload (str): The decoded payload

    Raises:
        - AuthError (400):
            - If there is no token found or is unable to parse the token
            - If kid doesn't match

        - AuthError (401):
            - If kid is not found
            - If token has expired
            - If there's an incorrect claim
    """
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Error decoding token headers.'
        }, 400)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. \
                    Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


def requires_auth(permission=''):
    """
    Gets the token using get_token_auth_header function, decodes the jwt
    using the verify_decode_jwt function and validate claims and
     check the requested permission using the check_permissions function.

    Arguments:
        permission (str): The Auth0 RBAC permission

    Returns:
        - The decorator which passes the decoded payload to the
     decorated method
    """
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
