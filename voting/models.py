import datetime

from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class Proposal(models.Model):
    abstract = models.TextField()
    title = models.TextField()
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.title

    @property
    def score(self):
        return self.vote_set.filter(is_interested=True).count()


class Vote(models.Model):
    proposal = models.ForeignKey('Proposal')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    created_at = models.DateTimeField(default=datetime.datetime.now)
    is_interested = models.BooleanField(default=True)

    class Meta:
        unique_together = ('proposal', 'user')

    def __str__(self):
        args = [
            self.user.email,
            'interested' if self.is_interested else 'not interested',
            self.proposal.title,
        ]
        return '{} was {} in {}'.format(*args)


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """Creates and saves a User with the given email and password."""
        user = self.model(
            email=self.normalize_email(email),
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=datetime.datetime.now(),
            created_at=datetime.datetime.now(),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.TextField(db_index=True, unique=True)
    is_staff = models.BooleanField(default=False,
                                   help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField(default=True,
                                    help_text='Designates whether this user should be treated as '
                                              'active. Unselect this instead of deleting accounts.')
    created_at = models.DateTimeField(default=datetime.datetime.now, null=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
