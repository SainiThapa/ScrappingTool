from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import logout

class AutoLogout:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set session timeout in seconds (e.g., 2 hours)
        session_timeout = getattr(settings, 'SESSION_TIMEOUT', 60)

        if request.user.is_authenticated:
            now = timezone.now()
            last_activity = request.session.get('last_activity', now)

            # Check if the session should expire
            if (now - last_activity).total_seconds() > session_timeout:
                logout(request)
            else:
                request.session['last_activity'] = now

        response = self.get_response(request)
        return response
