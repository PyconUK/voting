from braces.views import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, View)

from .forms import RegisterForm
from .models import Proposal, Vote


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        proposals = Proposal.objects.exclude(vote__user=self.request.user)
        if not proposals:
            return super().get(request, *args, **kwargs)
        return redirect('proposal-detail', pk=proposals.order_by('?').first().pk)


class ProposalDetail(LoginRequiredMixin, DetailView):
    model = Proposal
    template_name = 'proposal_detail.html'


class ProposalVote(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        try:
            proposal = Proposal.objects.get(pk=self.kwargs['pk'])
        except Proposal.DoesNotExist:
            return redirect('/')  # FIXME: What should we do here?

        choice = self.request.POST.get('vote')
        if not choice:
            return redirect('/')  # FIXME: What should we do here?

        Vote.objects.create(
            proposal=proposal,
            user=self.request.user,
            is_interested=bool(int(choice)),
        )

        return redirect('/')


class RandomisedProposalList(LoginRequiredMixin, ListView):
    model = Proposal
    ordering = '?'
    template_name = 'proposal_list.html'

    def get_queryset(self):
        return super().get_queryset().exclude(vote__user=self.request.user)


class Register(CreateView):
    form_class = RegisterForm
    success_url = '/'
    template_name = 'register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid, save the associated model and authenticate user.
        """
        self.object = form.save()

        # authenticate and login the user
        new_user = authenticate(
            username=form.data['email'],
            password=form.data['password1'],
        )

        if new_user:
            # login the user to the session
            login(self.request, new_user)

        return redirect(self.get_success_url())
