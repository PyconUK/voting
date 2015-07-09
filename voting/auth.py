from django.contrib.auth.backends import ModelBackend

from .models import User


class TicketAuthBackend(ModelBackend):
    """Log in to Django without providing a password."""
    def authenticate(self, ticket_id=None):
        try:
            return User.objects.get(ticket_id=ticket_id)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
