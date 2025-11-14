import jwt
from django.shortcuts import HttpResponseRedirect, reverse
from django.conf import settings
from django.http import JsonResponse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_url_prefixes = (
            # Login URL is exempt
            reverse(settings.LOGIN_URL_NAME),
            # Login callback URL is exempt
            '/users/auth/saml/callback',
            # Any call to an API endpoint is exempt (API endpoints use JWT)
            '/api',
            # Health check endpoint accessible without authentication
            '/health-check'
        )

    def __call__(self, request):
        # API calls to any endpoint in "/api" do not require CAS authentication
        if not request.user.is_authenticated and not request.path_info.startswith(self.exempt_url_prefixes):
            # Redirect to the login URL, preserving the original path in the 'next' parameter
            return HttpResponseRedirect(f"{reverse(settings.LOGIN_URL_NAME)}?next={request.path_info}")

        response = self.get_response(request)
        return response


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # JWT token only used for REST API -- skip all other
        if not request.path.startswith('/api/'):
            return self.get_response(request)

        # Get token from the Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
        if len(auth_header) == 2 and auth_header[0].lower() == 'bearer':
            jwt_token = auth_header[1]
            if self.verify_jwt_token(jwt_token):
                # Token verified
                return  self.get_response(request)
            else:
                # Invalid token
                return JsonResponse({'error': 'Invalid token'}, status=401)
        else:
            # No JWT token in header
            return JsonResponse({'error': 'Authentication required'}, status=401)

    def verify_jwt_token(self, jwt_token):
        """
        Returns True if the provided JWT token is valid, False otherwise
        """
        try:
            payload = jwt.decode(jwt_token, settings.JWT_SECRET, algorithms=['HS256'])
            role = payload['role']
            return (role == 'rest_api')
        except (KeyError, jwt.ExpiredSignatureError, jwt.DecodeError):
            return False
