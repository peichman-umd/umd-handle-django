from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from umd_handle.api.models import JWTToken
import jwt
import time

class Command(BaseCommand):
    help = "Creates a JWT token for use with the REST API."

    def add_arguments(self, parser):
        parser.add_argument("description", nargs=1, type=str)
        pass

    def handle(self, *args, **options):
        token_description = options['description'][0]
        jwt_secret = settings.JWT_SECRET
        if not jwt_secret:
            raise CommandError("JWT Secret is not defined.")

        token = create_token(jwt_secret, token_description)
        self.stdout.write(token)

def create_token(jwt_secret, description):
    """
    Creates a token using the given JWT Secret and description, and stores it
    in the JWTToken table. Raises a CommandError if an error occurs.
    """
    jwt_secret = get_jwt_secret()
    payload = get_token_payload()
    token = generate_token(jwt_secret, payload)
    store_token(token, description)
    return token

# Retrieves the JWT secret, or raises an ArgumentError if not found
def get_jwt_secret():
    """
    Retrieves the JWT secret from the environment, or raises a CommandError if
    not found or empty.
    """
    jwt_secret = settings.JWT_SECRET
    if not jwt_secret:
        raise CommandError("JWT Secret is not defined.")
    return jwt_secret

def get_token_payload():
   """
   The payload the JWT token should contain.
   """
   payload = {
        'role': 'rest_api',
        # issued at (iat) - time in seconds since January 1, 1970
        'iat': time.time()
   }
   return payload

def generate_token(jwt_secret, payload):
  """
  Returns a JWT token created from the given JWT secret and payload.
  """
  return jwt.encode(payload, jwt_secret, algorithm="HS256")


def store_token(token, description):
  """
  Stores the token in the database with the given description
  """
  JWTToken.objects.create(token=token, description=description)
