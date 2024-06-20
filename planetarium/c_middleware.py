import logging
from django.contrib.auth import authenticate

logger = logging.getLogger(__name__)


class LogFailedLoginAttemptsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.failed_attempts = {}

    def __call__(self, request):
        response = self.get_response(request)
        if request.method == "POST" and request.path == "/user/token/":
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(request, username=email, password=password)

            if user is None:
                self.failed_attempts[email] = self.failed_attempts.get(email, 0) + 1

                if self.failed_attempts[email] >= 3:
                    logger.warning(f"{email} has failed to log in 3 or more times.")
        return response
