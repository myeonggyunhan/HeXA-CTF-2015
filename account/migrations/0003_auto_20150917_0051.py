# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_remove_account_admin_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='rank',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
