from .models import Proposal


def proposal_counters(request):
    if not request.user.is_authenticated():
        return {}

    proposals = Proposal.objects.all()
    total = proposals.count()
    remaining = proposals.exclude(vote__user=request.user).count()

    return {'total': total, 'remaining': remaining}
