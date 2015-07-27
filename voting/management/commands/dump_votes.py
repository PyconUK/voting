import csv
import sys

from django.core.management.base import BaseCommand
from django.db.models import Count, IntegerField, Sum, Value
from django.db.models.expressions import Case, When

from ...models import Proposal, User

class Command(BaseCommand):
    """Script to dump voting data to stdout in CSV format"""
    
    help = 'Dump voting data to stdout in CSV format'

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--users', action='store_true')
        group.add_argument('--proposals', action='store_true')

    def handle(self, *args, **options):
        if options['proposals']:
            attrs = ['title', 'num_votes', 'num_interested']
            qs = Proposal.objects.annotate(
                num_votes=Count('vote'),
                num_interested=Sum(
                    Case(
                        When(vote__is_interested=True, then=Value(1)),
                        default=Value(0),
                    ),
                    output_field=IntegerField(),
                )
            ).order_by('-num_interested')
        elif options['users']:
            attrs = ['email', 'last_login', 'num_votes', 'num_interested']
            qs = User.objects.filter(
                last_login__isnull=False 
            ).annotate(
                num_votes=Count('vote'),
                num_interested=Sum(
                    Case(
                        When(vote__is_interested=True, then=Value(1)),
                        default=Value(0),
                    ),
                    output_field=IntegerField(),
                )
            ).order_by('last_login')
        else:
            assert False
        
        writer = csv.writer(sys.stdout)
        writer.writerow(attrs)

        for obj in qs:
            writer.writerow([getattr(obj, attr) for attr in attrs])
