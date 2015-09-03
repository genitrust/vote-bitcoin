# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='VotingCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('createdOn', models.DateTimeField(auto_now_add=True)),
                ('expiresOn', models.DateTimeField(null=True)),
                ('publicKey', models.CharField(unique=True, max_length=35)),
                ('privateKey', models.CharField(default=None, max_length=52, null=True, blank=True)),
            ],
        ),
    ]
