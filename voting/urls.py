from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

from .views import Home, Register, VoteForProposal

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', Home.as_view(), name='home'),
    # url(r'^reviewed/$', ReviewedProposals.as_view(), name='reviewed-proposals'),

    url(r'^proposal/(?P<pk>\w+)/vote/$', VoteForProposal.as_view(), name='vote'),

    url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^register/$', Register.as_view(), name='register'),
]
