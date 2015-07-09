# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0003_user_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.TextField(blank=True, null=True),
        ),
    ]
