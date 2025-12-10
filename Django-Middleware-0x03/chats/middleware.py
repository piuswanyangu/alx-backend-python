from datetime import datetime, time
import logging

from django.http import HttpResponseForbidden

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"

        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response
    

# restricted acces
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # allowed access from 6pm to 9pm
        self.start_time = time(18,0)
        self.end_time = time(21,0)

    def __call__(self, request):
        current_time = datetime.now().time()
        # if the urrent time is out of  6-9pm deny acess
        if not (self.start_time <= current_time <= self.end_time):
            return HttpResponseForbidden("Acces to chat  is restricted at this time")
        
        return self.get_response(request)