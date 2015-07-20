from braces.views import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView, TemplateView, View

from .models import Proposal, Vote


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        proposals = Proposal.objects.exclude(vote__user=self.request.user)
        if not proposals:
            return super().get(request, *args, **kwargs)
        return redirect('proposal-detail', pk=proposals.order_by('?').first().pk)


class Login(TemplateView):
    http_method_names = ['get']
    template_name = 'unknown_user.html'

    def get(self, request, *args, **kwargs):
        """Log a user in using their ticket_id"""
        if not self.kwargs.get('ticket_id'):
            return super().get(request, *args, **kwargs)

        new_user = authenticate(username=self.kwargs['ticket_id'])

        if not new_user:
            return super().get(request, *args, **kwargs)

        login(self.request, new_user)
        return redirect('home')


class ProposalDetail(LoginRequiredMixin, DetailView):
    model = Proposal
    template_name = 'proposal_detail.html'

    def get_context_data(self, **context):
        context = super().get_context_data(**context)

        proposals = Proposal.objects.all()
        context['total'] = proposals.count()
        context['remaining'] = proposals.exclude(vote__user=self.request.user).count()

        return context


class ProposalVote(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        proposal = get_object_or_404(Proposal, pk=self.kwargs['pk'])

        choice = self.request.POST.get('vote')
        if not choice:
            return redirect('/')  # FIXME: What should we do here?

        Vote.objects.update_or_create(
            proposal=proposal,
            user=self.request.user,
            defaults={
                'is_interested': bool(int(choice)),
            },
        )

        return redirect('/')


class UnreviewedProposals(LoginRequiredMixin, ListView):
    model = Proposal
    ordering = '?'
    template_name = 'unreviewed_proposal_list.html'

    def get_queryset(self):
        return super().get_queryset().exclude(vote__user=self.request.user)

    def get_context_data(self, **context):
        context = super().get_context_data(**context)

        proposals = Proposal.objects.all()
        context['total'] = proposals.count()
        context['remaining'] = proposals.exclude(vote__user=self.request.user).count()

        return context


class ReviewedProposals(LoginRequiredMixin, ListView):
    model = Vote
    ordering = 'created_at'
    template_name = 'reviewed_proposal_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
