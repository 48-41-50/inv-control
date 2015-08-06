# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
import django.contrib.postgres.fields
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contracts',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(null=True)),
                ('map_url', models.URLField(max_length=256, null=True)),
                ('start_dt', models.DateField(auto_now_add=True)),
                ('end_dt', models.DateField(default=datetime.date(9999, 12, 31))),
                ('dropoff_dt', models.DateField(null=True)),
                ('pickup_dt', models.DateField(null=True)),
                ('contact_name', models.CharField(max_length=128)),
                ('contact_address1', models.CharField(max_length=256)),
                ('contact_address2', models.CharField(max_length=256, null=True)),
                ('contact_city', models.CharField(max_length=128)),
                ('contact_zipcode', models.CharField(max_length=9)),
                ('contact_telno', models.CharField(max_length=15)),
                ('contact_telno_type', models.CharField(choices=[('M', 'Mobile'), ('L', 'Land-Line')], default='M', max_length=1)),
                ('contact_email', models.EmailField(max_length=254, null=True)),
                ('created_ts', models.DateTimeField(auto_now_add=True)),
                ('modified_ts', models.DateTimeField(auto_now=True)),
                ('items', django.contrib.postgres.fields.ArrayField(base_field=models.UUIDField(), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('name', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(null=True)),
                ('manufacturer', models.CharField(max_length=128)),
                ('height', models.DecimalField(null=True, max_digits=7, decimal_places=2)),
                ('width', models.DecimalField(null=True, max_digits=7, decimal_places=2)),
                ('depth', models.DecimalField(null=True, max_digits=7, decimal_places=2)),
                ('unit_measure', models.CharField(choices=[('I', 'Inches'), ('F', 'Feet'), ('C', 'Centimeters'), ('M', 'Meters')], null=True, default='F', max_length=1)),
                ('location', models.UUIDField()),
                ('location_type', models.CharField(choices=[('W', 'Warehouse'), ('I', 'In-Transit'), ('C', 'On Contract')], max_length=1)),
                ('purchase_dt', models.DateField(null=True)),
                ('active', models.BooleanField(default=True)),
                ('image', models.ImageField(height_field=300, width_field=300, null=True, upload_to='items')),
                ('created_ts', models.DateTimeField(auto_now_add=True)),
                ('modified_ts', models.DateTimeField(auto_now=True)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Pulls',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4, serialize=False)),
                ('from_location', models.UUIDField()),
                ('from_location_type', models.CharField(choices=[('W', 'Warehouse'), ('I', 'In-Transit'), ('C', 'On Contract')], max_length=1)),
                ('to_location', models.UUIDField()),
                ('to_location_type', models.CharField(choices=[('W', 'Warehouse'), ('I', 'In-Transit'), ('C', 'On Contract')], max_length=1)),
                ('start_dt', models.DateField(auto_now_add=True)),
                ('end_dt', models.DateField(default=datetime.date(9999, 12, 31))),
                ('created_ts', models.DateTimeField(auto_now_add=True)),
                ('modified_ts', models.DateTimeField(auto_now=True)),
                ('items', django.contrib.postgres.fields.ArrayField(base_field=models.UUIDField(), size=None)),
                ('contract', models.ForeignKey(to='invtrack.Contracts')),
            ],
        ),
        migrations.CreateModel(
            name='States',
            fields=[
                ('abbr', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=75)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4, serialize=False)),
                ('userid', models.CharField(max_length=25)),
                ('surname', models.CharField(max_length=50)),
                ('midname', models.CharField(max_length=50, null=True)),
                ('forename', models.CharField(max_length=50)),
                ('address1', models.CharField(max_length=256)),
                ('address2', models.CharField(max_length=256, null=True)),
                ('city', models.CharField(max_length=128)),
                ('zipcode', models.CharField(max_length=9)),
                ('telno', models.CharField(max_length=15)),
                ('telno_type', models.CharField(choices=[('M', 'Mobile'), ('L', 'Land-Line')], default='M', max_length=1)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('active', models.BooleanField(default=True)),
                ('start_dt', models.DateField(auto_now_add=True)),
                ('end_dt', models.DateField(default=datetime.date(9999, 12, 31))),
                ('image', models.ImageField(height_field=100, width_field=100, null=True, upload_to='users')),
                ('created_by', models.UUIDField()),
                ('created_ts', models.DateTimeField(auto_now_add=True)),
                ('modified_by', models.UUIDField()),
                ('modified_ts', models.DateTimeField(auto_now=True)),
                ('groups', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=25), size=None)),
                ('state', models.ForeignKey(to='invtrack.States')),
            ],
        ),
        migrations.CreateModel(
            name='WarehouseContainers',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4, serialize=False)),
                ('parent', models.UUIDField()),
                ('parent_type', models.CharField(choices=[('W', 'Warehouse'), ('F', 'Floor'), ('A', 'Area'), ('R', 'Rack'), ('S', 'Shelf'), ('B', 'Bin'), ('C', 'Section')], max_length=1)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(null=True)),
                ('height', models.DecimalField(null=True, max_digits=7, decimal_places=2)),
                ('width', models.DecimalField(null=True, max_digits=7, decimal_places=2)),
                ('depth', models.DecimalField(null=True, max_digits=7, decimal_places=2)),
                ('unit_measure', models.CharField(choices=[('I', 'Inches'), ('F', 'Feet'), ('C', 'Centimeters'), ('M', 'Meters')], null=True, default='F', max_length=1)),
                ('image', models.ImageField(height_field=300, width_field=300, null=True, upload_to='warehouse_containers')),
                ('created_ts', models.DateTimeField(auto_now_add=True)),
                ('modified_ts', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(to='invtrack.Users', related_name='whse_containers_created_by')),
                ('modified_by', models.ForeignKey(to='invtrack.Users', related_name='whse_containers_modified_by')),
            ],
        ),
        migrations.CreateModel(
            name='Warehouses',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField(null=True)),
                ('address1', models.CharField(max_length=256)),
                ('address2', models.CharField(max_length=256, null=True)),
                ('city', models.CharField(max_length=128)),
                ('zipcode', models.CharField(max_length=9)),
                ('telno', models.CharField(max_length=15)),
                ('telno_type', models.CharField(choices=[('M', 'Mobile'), ('L', 'Land-Line')], default='L', max_length=1)),
                ('map_url', models.URLField(max_length=256, null=True)),
                ('height', models.DecimalField(null=True, max_digits=7, decimal_places=2)),
                ('width', models.DecimalField(null=True, max_digits=7, decimal_places=2)),
                ('depth', models.DecimalField(null=True, max_digits=7, decimal_places=2)),
                ('unit_measure', models.CharField(choices=[('I', 'Inches'), ('F', 'Feet'), ('C', 'Centimeters'), ('M', 'Meters')], null=True, default='F', max_length=1)),
                ('start_dt', models.DateField(auto_now_add=True)),
                ('end_dt', models.DateField(default=datetime.date(9999, 12, 31))),
                ('image', models.ImageField(height_field=300, width_field=300, null=True, upload_to='warehouses')),
                ('created_ts', models.DateTimeField(auto_now_add=True)),
                ('modified_ts', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(to='invtrack.Users', related_name='warehouses_created_by')),
                ('modified_by', models.ForeignKey(to='invtrack.Users', related_name='warehouses_modified_by')),
                ('state', models.ForeignKey(to='invtrack.States')),
            ],
        ),
        migrations.AddField(
            model_name='warehousecontainers',
            name='warehouse',
            field=models.ForeignKey(to='invtrack.Warehouses'),
        ),
        migrations.AddField(
            model_name='pulls',
            name='created_by',
            field=models.ForeignKey(to='invtrack.Users', related_name='pulls_created_by'),
        ),
        migrations.AddField(
            model_name='pulls',
            name='modified_by',
            field=models.ForeignKey(to='invtrack.Users', related_name='pulls_modified_by'),
        ),
        migrations.AddField(
            model_name='items',
            name='created_by',
            field=models.ForeignKey(to='invtrack.Users', related_name='items_created_by'),
        ),
        migrations.AddField(
            model_name='items',
            name='modified_by',
            field=models.ForeignKey(to='invtrack.Users', related_name='items_modified_by'),
        ),
        migrations.AddField(
            model_name='contracts',
            name='company_contact',
            field=models.ForeignKey(to='invtrack.Users'),
        ),
        migrations.AddField(
            model_name='contracts',
            name='contact_state',
            field=models.ForeignKey(to='invtrack.States'),
        ),
        migrations.AddField(
            model_name='contracts',
            name='created_by',
            field=models.ForeignKey(to='invtrack.Users', related_name='contracts_created_by'),
        ),
        migrations.AddField(
            model_name='contracts',
            name='modified_by',
            field=models.ForeignKey(to='invtrack.Users', related_name='contracts_modified_by'),
        ),
    ]
