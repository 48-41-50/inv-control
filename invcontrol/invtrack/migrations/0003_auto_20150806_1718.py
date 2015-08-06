# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('invtrack', '0002_auto_20150806_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='contracts',
            name='invoice_number',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contracts',
            name='end_dt',
            field=models.DateField(default=datetime.date(9999, 12, 31), db_index=True),
        ),
        migrations.AlterField(
            model_name='contracts',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='contracts',
            name='start_dt',
            field=models.DateField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='items',
            name='active',
            field=models.BooleanField(default=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='pulls',
            name='end_dt',
            field=models.DateField(default=datetime.date(9999, 12, 31), db_index=True),
        ),
        migrations.AlterField(
            model_name='pulls',
            name='start_dt',
            field=models.DateField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='active',
            field=models.BooleanField(default=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='userid',
            field=models.CharField(max_length=25, unique=True),
        ),
        migrations.AlterField(
            model_name='warehouses',
            name='end_dt',
            field=models.DateField(default=datetime.date(9999, 12, 31), db_index=True),
        ),
        migrations.AlterField(
            model_name='warehouses',
            name='name',
            field=models.CharField(max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name='warehouses',
            name='start_dt',
            field=models.DateField(auto_now_add=True, db_index=True),
        ),
        migrations.RunSQL("create index invtrack_contract_items_ix on invtrack_contracts using gin (items);"),
        migrations.RunSQL("create index invtrack_pull_items_ix on invtrack_pulls using gin (items);"),
        migrations.RunSQL("create index invtrack_item_tags_ix on invtrack_items using gin (tags);"),
        migrations.RunSQL("create index invtrack_user_groups_ix on invtrack_users using gin (groups);"),
    ]
