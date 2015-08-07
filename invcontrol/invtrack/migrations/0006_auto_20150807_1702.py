# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invtrack', '0005_auto_20150807_1659'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='contract',
            table='invtrack_contracts',
        ),
        migrations.AlterModelTable(
            name='item',
            table='invtrack_items',
        ),
        migrations.AlterModelTable(
            name='pull',
            table='invtrack_pulls',
        ),
        migrations.AlterModelTable(
            name='state',
            table='invtrack_states',
        ),
        migrations.AlterModelTable(
            name='warehouse',
            table='invtrack_warehouses',
        ),
        migrations.AlterModelTable(
            name='warehousecontainer',
            table='invtrack_warehouse_containers',
        ),
    ]
