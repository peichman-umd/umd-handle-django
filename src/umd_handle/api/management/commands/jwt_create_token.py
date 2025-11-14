from django.core.management.base import BaseCommand
from umd_handle.api.tokens import create_jwt_token

class Command(BaseCommand):
    help = "Creates a JWT token for use with the REST API."

    def add_arguments(self, parser):
        parser.add_argument("description", nargs=1, type=str)
        pass

    def handle(self, *args, **options):
        token_description = options['description'][0]

        token = create_jwt_token(token_description)
        self.stdout.write(token)
