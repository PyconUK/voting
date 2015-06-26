from django.contrib import admin

from .models import Proposal, Vote


admin.site.register(Proposal)
admin.site.register(Vote)
