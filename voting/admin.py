from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import Count, ExpressionWrapper, F, IntegerField, Sum
from django.db.models.functions import Coalesce

from .models import Proposal, User, Vote


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ['title', 'num_votes', 'num_interested']
    search_fields = ['author', 'title', 'abstract']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            num_votes=Count('vote'),
            num_interested=Sum('vote__is_interested')
        ).order_by('-num_interested')

    def num_votes(self, proposal):
        return proposal.num_votes
    num_votes.short_description = 'Votes'

    def num_interested(self, proposal):
        return proposal.num_interested
    num_interested.short_description = 'Score'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'last_login', 'num_votes', 'num_interested', 'num_not_interested']
    search_fields = ['email', 'name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            num_votes=Count('vote'),
            num_interested=Sum(Coalesce('vote__is_interested', 0)),
        ).annotate(
            num_not_interested=ExpressionWrapper(
                F('num_votes') - F('num_interested'),
                output_field=IntegerField()
            )
        )

    def num_votes(self, user):
        return user.num_votes
    num_votes.short_description = 'Votes'

    def num_interested(self, user):
        return user.num_interested
    num_interested.short_description = 'Interested'

    def num_not_interested(self, user):
        return user.num_not_interested
    num_not_interested.short_description = 'Not interested'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_select_related = True


admin.site.unregister(Group)
