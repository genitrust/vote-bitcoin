# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votebitcoin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='publicKey',
            field=models.CharField(default='', unique=True, max_length=35),
            preserve_default=False,
        ),
    ]
