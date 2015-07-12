import uuid


def generate_user_token():
    """
    Generate a random token for a user

    This is wrapped in a function so Django can serialize it as a default
    in migrations.

    https://docs.djangoproject.com/en/1.8/topics/migrations/#migration-serializing
    """
    return uuid.uuid4()
