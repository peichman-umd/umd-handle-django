import jwt
import time
from django.conf import settings
from umd_handle.api.models import JWTToken

def create_jwt_token(description):
    """
    Creates a token using the given description, and stores it
    in the JWTToken table. Raises a KeyError if the "JWT_SECRET" setting
    is not set.
    """
    jwt_secret = _get_jwt_secret()
    payload = _get_token_payload()
    token = _generate_token(jwt_secret, payload)
    _store_token(token, description)
    return token

def _get_jwt_secret():
    """
    Retrieves the JWT secret from the environment, or raises a KeyError if
    not found or empty.
    """
    jwt_secret = settings.JWT_SECRET
    if not jwt_secret:
        raise KeyError("JWT Secret is not defined.")
    return jwt_secret

def _get_token_payload():
   """
   The payload the JWT token should contain.
   """
   payload = {
        'role': 'rest_api',
        # issued at (iat) - time in seconds since January 1, 1970
        'iat': time.time()
   }
   return payload

def _generate_token(jwt_secret, payload):
  """
  Returns a JWT token created from the given JWT secret and payload.
  """
  return jwt.encode(payload, jwt_secret, algorithm="HS256")


def _store_token(token, description):
  """
  Stores the token in the database with the given description
  """
  JWTToken.objects.create(token=token, description=description)
