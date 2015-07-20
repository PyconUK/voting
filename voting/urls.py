from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView

from .views import Home, Login, ProposalDetail, ProposalVote, ReviewedProposals

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^favicon.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico')),

    url(r'^$', Home.as_view(), name='home'),
    url(r'^reviewed/$', ReviewedProposals.as_view(), name='reviewed-proposals'),
    url(r'^unreviewed/$', UnreviewedProposals.as_view(), name='unreviewed-proposals'),

    url(r'^proposals/(?P<pk>\w+)/', include([
        url(r'^$', ProposalDetail.as_view(), name='proposal-detail'),
        url(r'^vote/$', ProposalVote.as_view(), name='vote'),
    ])),

    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^login/(?P<ticket_id>[\w-]+)/$', Login.as_view(), name='login'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
