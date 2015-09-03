# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votebitcoin', '0002_candidate_publickey'),
    ]

    operations = [
        migrations.AddField(
            model_name='votingcard',
            name='candidate',
            field=models.ForeignKey(default=None, blank=True, to='votebitcoin.Candidate', null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='publicKey',
            field=models.CharField(help_text=b'Should be unused.', unique=True, max_length=35),
        ),
    ]
