# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invtrack', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='created_by',
            field=models.ForeignKey(to='invtrack.Users', related_name='users_created_by'),
        ),
        migrations.AlterField(
            model_name='users',
            name='modified_by',
            field=models.ForeignKey(to='invtrack.Users', related_name='users_modified_by'),
        ),
        migrations.AlterField(
            model_name='warehousecontainers',
            name='parent',
            field=models.ForeignKey(to='invtrack.WarehouseContainers', related_name='whse_containers_parent'),
        ),
    ]
