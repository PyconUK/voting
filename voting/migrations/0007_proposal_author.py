# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0006_auto_20150709_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='author',
            field=models.TextField(null=True, blank=True),
        ),
    ]
