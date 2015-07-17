from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Proposal, User, Vote


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ['title', 'score']
    search_fields = ['author', 'title', 'abstract']


admin.site.register(User)
admin.site.register(Vote)

admin.site.unregister(Group)
