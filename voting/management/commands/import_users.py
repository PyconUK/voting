import csv

from django.core.management.base import BaseCommand

from ...models import User


class Command(BaseCommand):
    help = 'Import users from the specified csv'

    def add_arguments(self, parser):
        parser.add_argument('users_file')

    def handle(self, *args, **options):
        ignore_list = (
            'Conference Meal',
            'Scientist',
            'Teacher',
            'Young Person',
        )
        with open(options['users_file'], 'r') as f:
            for line in csv.DictReader(f):
                if line['Ticket'] in ignore_list:
                    continue

                name = line['Ticket Full Name']
                if not name:
                    name = line['Order Name']

                email = line['Ticket Email']
                if not email:
                    email = line['Order Email']

                ticket_id = line['Ticket Reference']

                if not (name or email):
                    print('Missing: {}'.format(ticket_id))
                    continue

                if User.objects.filter(ticket_id=ticket_id).exists():
                    print('User exists: {}'.format(email))
                    continue

                User.objects.create(
                    name=name,
                    email=email,
                    ticket_id=ticket_id,
                )
                print('User added: {}'.format(email))
