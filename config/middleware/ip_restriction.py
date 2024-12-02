from django.http import HttpResponseForbidden
from core.models import Ips


# Define allowed IPs
ips = list(Ips.objects.filter(active=True).values('ip'))
ALLOWED_IPS = []
for i in ips:
    ALLOWED_IPS.append(i['ip'])
    
def ip_restriction_middleware(get_response):
    def middleware(request):
        # Get client IP
        ip = get_client_ip(request)
        # Check if the IP and request path are allowed
        if not ip_allowed(ip, request):
            return HttpResponseForbidden("Access denied.")
        return get_response(request)

    return middleware

def get_client_ip(request):
    """
    Retrieve the client's IP address from the request.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        print(x_forwarded_for)
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def ip_allowed(ip, request):
    """
    Check if the IP and request are allowed.
    """
    # Allow POST requests from any IP for API endpoints
    if request.path.startswith('/hrm/api/') and request.method == "POST":
        return True
    
    print(ALLOWED_IPS)
    # Restrict other routes to allowed IPs
    return ip in ALLOWED_IPS
