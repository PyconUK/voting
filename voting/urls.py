from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login

from .views import Home, Register, VoteForProposal

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', Home.as_view(), name='home'),
    # url(r'^reviewed/$', ReviewedProposals.as_view(), name='reviewed-proposals'),

    url(r'^proposal/(?P<pk>\w+)/vote/$', VoteForProposal.as_view(), name='vote'),

    url(r'^register/$', Register.as_view(), name='register'),
    # url(r'^login/$', login(), name='login'),
]
