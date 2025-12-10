from datetime import datetime, time
import logging
from django.http import HttpResponseForbidden, JsonResponse

logger = logging.getLogger(__name__)

# ============================================================
# 1. REQUEST LOGGING MIDDLEWARE
# Logs every incoming request to request_logs.log
# ============================================================
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log user identity (Authenticated or Anonymous)
        user = request.user if request.user.is_authenticated else "Anonymous"

        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)


# ============================================================
# 2. TIME-BASED ACCESS RESTRICTION MIDDLEWARE
# Restricts chat access to between 6PM (18:00) and 9PM (21:00)
# ============================================================
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Allowed access window: 6pm–9pm
        self.start_time = time(18, 0)
        self.end_time = time(21, 0)

    def __call__(self, request):
        current_time = datetime.now().time()

        # Deny access if current time is OUTSIDE allowed window
        if not (self.start_time <= current_time <= self.end_time):
            return HttpResponseForbidden(
                "Access to chat is restricted at this time"
            )

        return self.get_response(request)


# ============================================================
# 3. OFFENSIVE LANGUAGE / RATE LIMITING MIDDLEWARE
# Limits users to 5 POST messages per minute based on IP address
# ============================================================
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Dictionary to track timestamps of messages per IP
        # Example: {"127.0.0.1": [timestamp1, timestamp2, ...]}
        self.ip_tracker = {}

        # Rate-limit settings
        self.time_window = 60     # time window: 1 minute
        self.max_messages = 5     # max 5 messages per minute

    def __call__(self, request):
        ip = self.get_client_ip(request)

        # Middleware only monitors POST requests (sending messages)
        if request.method == "POST":
            now = time.time()
            timestamps = self.ip_tracker.get(ip, [])

            # Keep only timestamps within the last 60 seconds
            timestamps = [
                t for t in timestamps
                if now - t < self.time_window
            ]

            # If message count exceeds limit → reject
            if len(timestamps) >= self.max_messages:
                return JsonResponse(
                    {"error": "Rate limit exceeded. Try again later."},
                    status=429  # Too Many Requests
                )

            # Log new timestamp
            timestamps.append(now)
            self.ip_tracker[ip] = timestamps

        return self.get_response(request)

    def get_client_ip(self, request):
        """Extract client IP from request headers."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")

# ============================================================
# 4. ROLE-BASED PERMISSION MIDDLEWARE
# Blocks users who are NOT admin or moderator
# ============================================================

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Check if the user has admin privileges.
        We assume the User model has a field: role = ('admin', 'moderator', 'user')
        """

        # Only check if the user is authenticated
        if request.user.is_authenticated:

            # Get the role from the user model
            user_role = getattr(request.user, "role", None)

            # Block if user is not admin or moderator
            if user_role not in ["admin", "moderator"]:
                return JsonResponse(
                    {"error": "You do not have permission to perform this action."},
                    status=403
                )

        return self.get_response(request)
