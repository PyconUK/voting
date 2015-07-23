from .models import Proposal


def proposal_counters(request):
    if not request.user.is_authenticated():
        return {}

    num_proposals = Proposal.objects.count()

    counters = {
        'num_remaining': num_proposals - request.user.num_votes,
        'num_interested': request.user.num_interested,
        'num_not_interested': request.user.num_not_interested,
    }

    return counters
