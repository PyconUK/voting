from .models import Proposal


def proposal_counters(request):
    proposals = Proposal.objects.all()
    total = proposals.count()
    remaining = proposals.exclude(vote__user=request.user).count()

    return {'total': total, 'remaining': remaining}
