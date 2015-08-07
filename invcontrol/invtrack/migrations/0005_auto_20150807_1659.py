# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields
from django.conf import settings
import datetime
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('invtrack', '0004_auto_20150806_2043'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('address1', models.CharField(max_length=256)),
                ('address2', models.CharField(null=True, max_length=256)),
                ('city', models.CharField(max_length=128)),
                ('zipcode', models.CharField(max_length=9)),
                ('telno', models.CharField(max_length=15)),
                ('telno_type', models.CharField(default='M', choices=[('M', 'Mobile'), ('L', 'Land-Line')], max_length=1)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('description', models.TextField(null=True)),
                ('invoice_number', models.CharField(null=True, max_length=50)),
                ('map_url', models.URLField(null=True, max_length=256)),
                ('start_dt', models.DateField(db_index=True, auto_now_add=True)),
                ('end_dt', models.DateField(default=datetime.date(9999, 12, 31), db_index=True)),
                ('dropoff_dt', models.DateField(null=True)),
                ('pickup_dt', models.DateField(null=True)),
                ('contact_name', models.CharField(max_length=128)),
                ('contact_email', models.EmailField(null=True, max_length=254)),
                ('created_ts', models.DateTimeField(auto_now_add=True)),
                ('modified_ts', models.DateTimeField(auto_now=True)),
                ('items', django.contrib.postgres.fields.ArrayField(base_field=models.UUIDField(), size=None)),
                ('company_contact', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(related_name='contract_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='contract_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['start_dt', 'invoice_number', 'name'],
                'db_table': 'contracts',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(null=True)),
                ('manufacturer', models.CharField(max_length=128)),
                ('height', models.DecimalField(max_digits=7, null=True, decimal_places=2)),
                ('width', models.DecimalField(max_digits=7, null=True, decimal_places=2)),
                ('depth', models.DecimalField(max_digits=7, null=True, decimal_places=2)),
                ('unit_measure', models.CharField(default='F', null=True, choices=[('I', 'Inches'), ('F', 'Feet'), ('C', 'Centimeters'), ('M', 'Meters')], max_length=1)),
                ('location', models.UUIDField()),
                ('location_type', models.CharField(choices=[('W', 'Warehouse'), ('I', 'In-Transit'), ('C', 'On Contract')], max_length=1)),
                ('purchase_dt', models.DateField(null=True)),
                ('active', models.BooleanField(default=True, db_index=True)),
                ('image', models.ImageField(height_field=300, null=True, width_field=300, upload_to='items')),
                ('created_ts', models.DateTimeField(auto_now_add=True)),
                ('modified_ts', models.DateTimeField(auto_now=True)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), size=None)),
                ('created_by', models.ForeignKey(related_name='item_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='item_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'items',
            },
        ),
        migrations.CreateModel(
            name='Pull',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('from_location', models.UUIDField()),
                ('from_location_type', models.CharField(choices=[('W', 'Warehouse'), ('I', 'In-Transit'), ('C', 'On Contract')], max_length=1)),
                ('to_location', models.UUIDField()),
                ('to_location_type', models.CharField(choices=[('W', 'Warehouse'), ('I', 'In-Transit'), ('C', 'On Contract')], max_length=1)),
                ('start_dt', models.DateField(db_index=True, auto_now_add=True)),
                ('end_dt', models.DateField(default=datetime.date(9999, 12, 31), db_index=True)),
                ('created_ts', models.DateTimeField(auto_now_add=True)),
                ('modified_ts', models.DateTimeField(auto_now=True)),
                ('items', django.contrib.postgres.fields.ArrayField(base_field=models.UUIDField(), size=None)),
                ('contract', models.ForeignKey(to='invtrack.Contract')),
                ('created_by', models.ForeignKey(related_name='pull_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='pull_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['start_dt'],
                'db_table': 'pulls',
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('address1', models.CharField(max_length=256)),
                ('address2', models.CharField(null=True, max_length=256)),
                ('city', models.CharField(max_length=128)),
                ('zipcode', models.CharField(max_length=9)),
                ('telno', models.CharField(max_length=15)),
                ('telno_type', models.CharField(default='M', choices=[('M', 'Mobile'), ('L', 'Land-Line')], max_length=1)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('description', models.TextField(null=True)),
                ('map_url', models.URLField(null=True, max_length=256)),
                ('height', models.DecimalField(max_digits=7, null=True, decimal_places=2)),
                ('width', models.DecimalField(max_digits=7, null=True, decimal_places=2)),
                ('depth', models.DecimalField(max_digits=7, null=True, decimal_places=2)),
                ('unit_measure', models.CharField(default='F', null=True, choices=[('I', 'Inches'), ('F', 'Feet'), ('C', 'Centimeters'), ('M', 'Meters')], max_length=1)),
                ('start_dt', models.DateField(db_index=True, auto_now_add=True)),
                ('end_dt', models.DateField(default=datetime.date(9999, 12, 31), db_index=True)),
                ('image', models.ImageField(height_field=300, null=True, width_field=300, upload_to='warehouses')),
                ('created_ts', models.DateTimeField(auto_now_add=True)),
                ('modified_ts', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(related_name='warehouse_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='warehouse_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['city', 'name'],
                'db_table': 'warehouses',
            },
        ),
        migrations.CreateModel(
            name='WarehouseContainer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('parent_type', models.CharField(choices=[('9', 'Floor'), ('8', 'Area'), ('7', 'Rack'), ('6', 'Shelf'), ('5', 'Bin'), ('5', 'Section')], max_length=1)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(null=True)),
                ('height', models.DecimalField(max_digits=7, null=True, decimal_places=2)),
                ('width', models.DecimalField(max_digits=7, null=True, decimal_places=2)),
                ('depth', models.DecimalField(max_digits=7, null=True, decimal_places=2)),
                ('unit_measure', models.CharField(default='F', null=True, choices=[('I', 'Inches'), ('F', 'Feet'), ('C', 'Centimeters'), ('M', 'Meters')], max_length=1)),
                ('image', models.ImageField(height_field=300, null=True, width_field=300, upload_to='warehouse_containers')),
                ('created_ts', models.DateTimeField(auto_now_add=True)),
                ('modified_ts', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(related_name='whse_container_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='whse_container_modified_by', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(related_name='whse_container_parent', to='invtrack.WarehouseContainer')),
                ('warehouse', models.ForeignKey(to='invtrack.Warehouse')),
            ],
            options={
                'db_table': 'warehouse_containers',
            },
        ),
        migrations.RenameModel(
            old_name='States',
            new_name='State',
        ),
        migrations.RemoveField(
            model_name='contracts',
            name='company_contact',
        ),
        migrations.RemoveField(
            model_name='contracts',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='contracts',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='contracts',
            name='state',
        ),
        migrations.DeleteModel(
            name='Groups',
        ),
        migrations.RemoveField(
            model_name='items',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='items',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='pulls',
            name='contract',
        ),
        migrations.RemoveField(
            model_name='pulls',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='pulls',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='users',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='users',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='users',
            name='state',
        ),
        migrations.RemoveField(
            model_name='warehousecontainers',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='warehousecontainers',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='warehousecontainers',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='warehousecontainers',
            name='warehouse',
        ),
        migrations.RemoveField(
            model_name='warehouses',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='warehouses',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='warehouses',
            name='state',
        ),
        migrations.AlterModelTable(
            name='state',
            table='states',
        ),
        migrations.DeleteModel(
            name='Contracts',
        ),
        migrations.DeleteModel(
            name='Items',
        ),
        migrations.DeleteModel(
            name='Pulls',
        ),
        migrations.DeleteModel(
            name='Users',
        ),
        migrations.DeleteModel(
            name='WarehouseContainers',
        ),
        migrations.DeleteModel(
            name='Warehouses',
        ),
        migrations.AddField(
            model_name='warehouse',
            name='state',
            field=models.ForeignKey(to='invtrack.State'),
        ),
        migrations.AddField(
            model_name='contract',
            name='state',
            field=models.ForeignKey(to='invtrack.State'),
        ),
    ]
