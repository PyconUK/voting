from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.generic import RedirectView

from .views import Home, ProposalDetail, Register, ProposalVote

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^favicon.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico')),

    # url(r'^$', RandomisedProposalList.as_view(), name='home'),
    url(r'^$', Home.as_view(), name='home'),
    # url(r'^reviewed/$', ReviewedProposals.as_view(), name='reviewed-proposals'),

    url(r'^proposals/(?P<pk>\w+)/', include([
        url(r'^$', ProposalDetail.as_view(), name='proposal-detail'),
        url(r'^vote/$', ProposalVote.as_view(), name='vote'),
    ])),

    url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^register/$', Register.as_view(), name='register'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
