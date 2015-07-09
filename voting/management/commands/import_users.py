import csv

from django.core.management.base import BaseCommand

from ...models import User


class Command(BaseCommand):
    """
    Generate a csv from the tito output csv using:

    awk '{print $4 "," $7 "," $11}' FPAT="([^,]*)|(\"[^\"]+\")" input.csv | tail -n +2 > output.csv

    Import to the voting app with this command.
    """
    help = 'Import users from the specified csv'

    def add_arguments(self, parser):
        parser.add_argument('users_file')

    def handle(self, *args, **options):
        with open(options['users_file'], 'r') as f:
            for name, email, ticket_id in csv.reader(f):
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
