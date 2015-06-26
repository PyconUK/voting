import re

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect


# exempt login and logout
EXEMPT_URLS = [
    re.compile('^{}$'.format(settings.LOGIN_URL.lstrip('/'))),
    re.compile('^{}$'.format(settings.LOGOUT_URL.lstrip('/'))),
]


class LoginRequiredMiddleware:
    def process_request(self, request):
        # Jump over this middleware if not a protected url.
        path = request.path_info.lstrip('/')
        if any(m.match(path) for m in EXEMPT_URLS):
            return

        # Jump over this middleware if user logged in.
        if request.user.is_authenticated():
            return

        # Add a message, and redirect to login.
        messages.info(request, 'You must be logged in to view this page.')
        return HttpResponseRedirect(settings.LOGIN_URL + '?next=' + request.path_info)
