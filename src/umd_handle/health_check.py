from django.http import HttpResponse

def health_check(request):
    """
    Simple health check endpoint that returns an HTTP 200 OK response.
    """
    return HttpResponse("OK", status=200)