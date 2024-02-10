import pytz
from django.utils import timezone
from django.core.cache import cache


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            user_id = user.id

            # this cached data is stored in django server
            # thats why even if some other user changes timezone of someone,
            # it would reflect to that person
            cached_timezone = cache.get(f"user_timezone_{user_id}")
            if cached_timezone:
                timezone.activate(pytz.timezone(cached_timezone))
            else:
                preferred_timezone = user.prefered_time_zone
                cache.set(f"user_timezone_{user_id}", preferred_timezone)
                timezone.activate(pytz.timezone(preferred_timezone))
        return self.get_response(request)
