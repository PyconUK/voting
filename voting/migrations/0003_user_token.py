# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import voting.utils


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0002_add_vote_unique_constraints'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.TextField(null=True, blank=True, unique=True, db_index=True, default=voting.utils.generate_user_token),
        ),
    ]
