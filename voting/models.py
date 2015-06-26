import datetime

from django.db import models
from django.conf import settings


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

    def __str__(self):
        args = [
            self.user.email,
            'interested' if self.is_interested else 'not interested',
            self.proposal.title,
        ]
        return '{} was {} in {}'.format(*args)
