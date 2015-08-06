# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invtrack', '0003_auto_20150806_1718'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contracts',
            options={'ordering': ['start_dt', 'invoice_number', 'name']},
        ),
        migrations.AlterModelOptions(
            name='pulls',
            options={'ordering': ['start_dt']},
        ),
        migrations.AlterModelOptions(
            name='users',
            options={'ordering': ['surname', 'forename']},
        ),
        migrations.AlterModelOptions(
            name='warehouses',
            options={'ordering': ['city', 'name']},
        ),
        migrations.RenameField(
            model_name='contracts',
            old_name='contact_address1',
            new_name='address1',
        ),
        migrations.RenameField(
            model_name='contracts',
            old_name='contact_address2',
            new_name='address2',
        ),
        migrations.RenameField(
            model_name='contracts',
            old_name='contact_city',
            new_name='city',
        ),
        migrations.RenameField(
            model_name='contracts',
            old_name='contact_state',
            new_name='state',
        ),
        migrations.RenameField(
            model_name='contracts',
            old_name='contact_telno',
            new_name='telno',
        ),
        migrations.RenameField(
            model_name='contracts',
            old_name='contact_telno_type',
            new_name='telno_type',
        ),
        migrations.RenameField(
            model_name='contracts',
            old_name='contact_zipcode',
            new_name='zipcode',
        ),
        migrations.AlterField(
            model_name='contracts',
            name='created_by',
            field=models.ForeignKey(related_name='contract_created_by', to='invtrack.Users'),
        ),
        migrations.AlterField(
            model_name='contracts',
            name='modified_by',
            field=models.ForeignKey(related_name='contract_modified_by', to='invtrack.Users'),
        ),
        migrations.AlterField(
            model_name='items',
            name='created_by',
            field=models.ForeignKey(related_name='item_created_by', to='invtrack.Users'),
        ),
        migrations.AlterField(
            model_name='items',
            name='modified_by',
            field=models.ForeignKey(related_name='item_modified_by', to='invtrack.Users'),
        ),
        migrations.AlterField(
            model_name='pulls',
            name='created_by',
            field=models.ForeignKey(related_name='pull_created_by', to='invtrack.Users'),
        ),
        migrations.AlterField(
            model_name='pulls',
            name='modified_by',
            field=models.ForeignKey(related_name='pull_modified_by', to='invtrack.Users'),
        ),
        migrations.AlterField(
            model_name='users',
            name='created_by',
            field=models.ForeignKey(related_name='user_created_by', to='invtrack.Users'),
        ),
        migrations.AlterField(
            model_name='users',
            name='modified_by',
            field=models.ForeignKey(related_name='user_modified_by', to='invtrack.Users'),
        ),
        migrations.AlterField(
            model_name='warehousecontainers',
            name='created_by',
            field=models.ForeignKey(related_name='whse_container_created_by', to='invtrack.Users'),
        ),
        migrations.AlterField(
            model_name='warehousecontainers',
            name='modified_by',
            field=models.ForeignKey(related_name='whse_container_modified_by', to='invtrack.Users'),
        ),
        migrations.AlterField(
            model_name='warehousecontainers',
            name='parent',
            field=models.ForeignKey(related_name='whse_container_parent', to='invtrack.WarehouseContainers'),
        ),
        migrations.AlterField(
            model_name='warehousecontainers',
            name='parent_type',
            field=models.CharField(choices=[('0', 'Warehouse'), ('1', 'Floor'), ('2', 'Area'), ('3', 'Rack'), ('4', 'Shelf'), ('5', 'Bin'), ('6', 'Section')], max_length=1),
        ),
        migrations.AlterField(
            model_name='warehouses',
            name='created_by',
            field=models.ForeignKey(related_name='warehouse_created_by', to='invtrack.Users'),
        ),
        migrations.AlterField(
            model_name='warehouses',
            name='modified_by',
            field=models.ForeignKey(related_name='warehouse_modified_by', to='invtrack.Users'),
        ),
        migrations.AlterField(
            model_name='warehouses',
            name='telno_type',
            field=models.CharField(default='M', choices=[('M', 'Mobile'), ('L', 'Land-Line')], max_length=1),
        ),
    ]
