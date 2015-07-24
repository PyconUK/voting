from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import Count, ExpressionWrapper, F, IntegerField, Sum, Value
from django.db.models.expressions import Case, When
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
            num_interested=Sum(
                Case(When(vote__is_interested=True, then=Value(1))),
                output_field=IntegerField(),
            )
        ).order_by('-num_interested')

    def num_votes(self, proposal):
        return proposal.num_votes
    num_votes.short_description = 'Votes'

    def num_interested(self, proposal):
        return proposal.num_interested
    num_interested.short_description = 'Score'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'last_login', 'vote_count', 'interested_count', 'not_interested_count']
    search_fields = ['email', 'name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            vote_count=Count('vote'),
            interested_count=Sum(
                Case(When(vote__is_interested=True, then=Value(1))),
                output_field=IntegerField(),
            )
        ).annotate(
            not_interested_count=ExpressionWrapper(
                F('vote_count') - F('interested_count'),
                output_field=IntegerField()
            )
        )

    def vote_count(self, user):
        return user.vote_count
    vote_count.short_description = 'Votes'

    def interested_count(self, user):
        return user.interested_count
    interested_count.short_description = 'Interested'

    def not_interested_count(self, user):
        return user.not_interested_count
    not_interested_count.short_description = 'Not interested'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_select_related = True


admin.site.unregister(Group)
