import os
import re

import requests
from django.core.management.base import BaseCommand, CommandError
from first import first

from ...models import Proposal


class Command(BaseCommand):
    """
    Script to import talk abstracts from the mail website repository

    Using the talk titles from the Selected Talks spreadsheet generate
    slugs so we can get the abstract from github.

    This script is designed to be run regularly.
    """
    help = 'Import talk abstracts from the main website repo'

    def handle(self, *args, **options):
        url = 'https://api.github.com/repos/pyconuk/pyconuk.org/contents/content/talks/'
        r = requests.get(url)
        r.raise_for_status()
        talks = r.json()

        s = requests.Session()

        # loop the talks from the csv/txt file
        with open('talk_titles.txt', 'r') as titles:
            for title in titles:
                # generate slugged titles
                tmp = re.sub('[^\w\s-]', '', title)
                slug = re.sub('[-\s]+', '-', tmp).strip('-').strip().lower()

                # get the download path for the abstract in the pyconuk repo
                talk_data = first(filter(lambda x: x['name'] == slug + '.md', talks))
                if not talk_data:
                    print('Talk not found: {}'.format(slug))
                    continue

                r = s.get(talk_data['download_url'])
                r.raise_for_status()

                # strip the wok metadata and title
                talk = r.text.split('\n')
                author = talk[7]
                abstract = '\n'.join(talk[9:])

                obj, created = Proposal.objects.update_or_create(
                    title=title,
                    defaults={'abstract': abstract, 'author': author},
                )
                print('{} Talk: {}'.format('Created' if created else 'Updated', title.strip()))
