from django.shortcuts import HttpResponseRedirect, reverse
from django.conf import settings

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
        )
    def __call__(self, request):
        # API calls to any endpoint in "/api" do not require CAS authentication
        if not request.user.is_authenticated and not request.path_info.startswith(self.exempt_url_prefixes):
            # Redirect to the login URL, preserving the original path in the 'next' parameter
            return HttpResponseRedirect(f"{reverse(settings.LOGIN_URL_NAME)}?next={request.path_info}")

        response = self.get_response(request)
        return response
