import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from django.core.cache import cache

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('requests.log')
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if current_hour < 18 or current_hour >= 21:  # Only allow access between 6PM (18) and 9PM (21)
            return HttpResponseForbidden("Access to chat is restricted during these hours.")
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.window = timedelta(minutes=1)
        self.limit = 5

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/api/messages/'):
            ip = self.get_client_ip(request)
            now = datetime.now()
            cache_key = f"msg_count_{ip}"
            msg_info = cache.get(cache_key, {'count': 0, 'start_time': now})

            if (now - msg_info['start_time']) > self.window:
                msg_info = {'count': 1, 'start_time': now}
            else:
                msg_info['count'] += 1

            if msg_info['count'] > self.limit:
                return HttpResponseForbidden("Too many messages. Try again later.")

            cache.set(cache_key, msg_info, timeout=60)
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_paths = ['/api/messages/', '/api/conversations/']
        if request.path.startswith(tuple(protected_paths)):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required.")
            user_role = getattr(request.user, 'role', 'user')
            if user_role not in ['admin', 'moderator']:
                return HttpResponseForbidden("Insufficient permissions.")
        return self.get_response(request)

