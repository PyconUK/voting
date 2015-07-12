from django.contrib.auth.backends import ModelBackend

from .models import User


class TicketAuthBackend(ModelBackend):
    """Log in to Django without providing a password."""
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(ticket_id=username)
        except User.DoesNotExist:
            return None

        # the admin form will send us a password to check too
        if password is not None and not user.check_password(password):
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
