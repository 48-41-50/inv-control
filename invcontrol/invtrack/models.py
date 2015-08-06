import uuid
import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

TELNO_CHOICES = (
    ('M', 'Mobile'),
    ('L', 'Land-Line'),
)


UOM_CHOICES = (
    ('I', 'Inches'),
    ('F', 'Feet'),
    ('C', 'Centimeters'),
    ('M', 'Meters'),
)


CONTAINER_CHOICES = (
    ('0', 'Warehouse'),
    ('1', 'Floor'),
    ('2', 'Area'),
    ('3', 'Rack'),
    ('4', 'Shelf'),
    ('5', 'Bin'),
    ('6', 'Section'),
)


LOCATION_CHOICES = (
    ('W', 'Warehouse'),
    ('I', 'In-Transit'),
    ('C', 'On Contract'),
)


class Addressable(models.Model):
    address1        = models.CharField(max_length=256, null=False, blank=False)
    address2        = models.CharField(max_length=256, null=True, blank=False)
    city            = models.CharField(max_length=128, null=False, blank=False)
    state           = models.ForeignKey("States", null=False, blank=False)
    zipcode         = models.CharField(max_length=9, null=False, blank=False)
    telno           = models.CharField(max_length=15, null=False, blank=False)
    telno_type      = models.CharField(max_length=1, null=False, blank=False, default=TELNO_CHOICES[0][0], choices=TELNO_CHOICES)
    
    class Meta:
        abstract    = True
    # End class Meta
# End class Address


class States(models.Model):
    abbr = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=75)
# End class States


class Groups(models.Model):
    name        = models.CharField(max_length=25, primary_key=True)
    description = models.CharField(max_length=100)
# End class Groups


class Users(Addressable):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userid          = models.CharField(max_length=25, null=False, blank=False, unique=True)
    surname         = models.CharField(max_length=50, null=False, blank=False)
    midname         = models.CharField(max_length=50, null=True, blank=False)
    forename        = models.CharField(max_length=50, null=False, blank=False)
    email           = models.EmailField(null=True, blank=False)
    active          = models.BooleanField(null=False, default=True, db_index=True)
    start_dt        = models.DateField(null=False, auto_now_add=True)
    end_dt          = models.DateField(null=False, default=datetime.date(9999, 12, 31))
    image           = models.ImageField(upload_to="users", null=True, height_field=100, width_field=100)
    created_by      = models.ForeignKey("self", related_name="user_created_by")
    created_ts      = models.DateTimeField(auto_now_add=True, null=False)
    modified_by     = models.ForeignKey("self", related_name="user_modified_by")
    modified_ts     = models.DateTimeField(auto_now=True, null=False)
    groups          = ArrayField(models.CharField(max_length=25, null=False), null=False)
    
    class Meta:
        ordering = ['surname', 'forename']
    # End class Meta
# End class Users


class Warehouses(Addressable):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name            = models.CharField(max_length=256, null=False, blank=False, unique=True)
    description     = models.TextField(null=True, blank=False)
    map_url         = models.URLField(max_length=256, null=True, blank=False)
    height          = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    width           = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    depth           = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    unit_measure    = models.CharField(max_length=1, null=True, blank=False, default=UOM_CHOICES[1][0], choices=UOM_CHOICES)
    start_dt        = models.DateField(null=False, auto_now_add=True, db_index=True)
    end_dt          = models.DateField(null=False, default=datetime.date(9999, 12, 31), db_index=True)
    image           = models.ImageField(upload_to="warehouses", null=True, height_field=300, width_field=300)
    created_by      = models.ForeignKey(Users, related_name='warehouse_created_by')
    created_ts      = models.DateTimeField(auto_now_add=True, null=False)
    modified_by     = models.ForeignKey(Users, related_name='warehouse_modified_by')
    modified_ts     = models.DateTimeField(auto_now=True, null=False)
    
    class Meta:
        ordering = ['city', 'name']
    # End class Meta
# End class Warehouses


class WarehouseContainers(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    warehouse       = models.ForeignKey(Warehouses, null=False)
    parent          = models.ForeignKey("self", related_name="whse_container_parent")
    parent_type     = models.CharField(max_length=1, null=False, blank=False, choices=CONTAINER_CHOICES)
    name            = models.CharField(max_length=128, null=False, blank=False)
    description     = models.TextField(null=True, blank=False)
    height          = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    width           = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    depth           = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    unit_measure    = models.CharField(max_length=1, null=True, blank=False, default=UOM_CHOICES[1][0], choices=UOM_CHOICES)
    image           = models.ImageField(upload_to="warehouse_containers", null=True, height_field=300, width_field=300)
    created_by      = models.ForeignKey(Users, related_name='whse_container_created_by')
    created_ts      = models.DateTimeField(auto_now_add=True, null=False)
    modified_by     = models.ForeignKey(Users, related_name='whse_container_modified_by')
    modified_ts     = models.DateTimeField(auto_now=True, null=False)
# End class WarehouseContainers


class Items(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name            = models.CharField(max_length=128, null=False, blank=False)
    description     = models.TextField(null=True, blank=False)
    manufacturer    = models.CharField(max_length=128, null=False, blank=False)
    height          = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    width           = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    depth           = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    unit_measure    = models.CharField(max_length=1, null=True, blank=False, default=UOM_CHOICES[1][0], choices=UOM_CHOICES)
    location        = models.UUIDField(null=False)
    location_type   = models.CharField(max_length=1, null=False, blank=False, choices=LOCATION_CHOICES)
    purchase_dt     = models.DateField(null=True)
    active          = models.BooleanField(null=False, default=True, db_index=True)
    image           = models.ImageField(upload_to="items", null=True, height_field=300, width_field=300)
    created_by      = models.ForeignKey(Users, related_name='item_created_by')
    created_ts      = models.DateTimeField(auto_now_add=True, null=False)
    modified_by     = models.ForeignKey(Users, related_name='item_modified_by')
    modified_ts     = models.DateTimeField(auto_now=True, null=False)
    tags            = ArrayField(models.CharField(max_length=50, null=False, blank=False))
    
    def get_location_path(self):
        pass
    # End get_location_path
# End class Items


class Contracts(Addressable):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name                    = models.CharField(max_length=128, null=False, blank=False, unique=True)
    description             = models.TextField(null=True, blank=False)
    invoice_number          = models.CharField(max_length=50, null=True, blank=False)
    map_url                 = models.URLField(max_length=256, null=True, blank=False)
    start_dt                = models.DateField(null=False, auto_now_add=True, db_index=True)
    end_dt                  = models.DateField(null=False, default=datetime.date(9999, 12, 31), db_index=True)
    dropoff_dt              = models.DateField(null=True)
    pickup_dt               = models.DateField(null=True)
    company_contact         = models.ForeignKey(Users, null=False)
    contact_name            = models.CharField(max_length=128, null=False)
    contact_email           = models.EmailField(null=True, blank=False)
    created_by              = models.ForeignKey(Users, related_name='contract_created_by')
    created_ts              = models.DateTimeField(auto_now_add=True, null=False)
    modified_by             = models.ForeignKey(Users, related_name='contract_modified_by')
    modified_ts             = models.DateTimeField(auto_now=True, null=False)
    items                   = ArrayField(models.UUIDField(null=False, blank=False))
    
    class Meta:
        ordering = ['start_dt', 'invoice_number', 'name']
    # End class Meta
# End class Contracts


class Pulls(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contract                = models.ForeignKey(Contracts, null=False, db_index=True)
    from_location           = models.UUIDField(null=False)
    from_location_type      = models.CharField(max_length=1, null=False, blank=False, choices=LOCATION_CHOICES)
    to_location             = models.UUIDField(null=False)
    to_location_type        = models.CharField(max_length=1, null=False, blank=False, choices=LOCATION_CHOICES)
    start_dt                = models.DateField(null=False, auto_now_add=True, db_index=True)
    end_dt                  = models.DateField(null=False, default=datetime.date(9999, 12, 31), db_index=True)
    created_by              = models.ForeignKey(Users, related_name='pull_created_by')
    created_ts              = models.DateTimeField(auto_now_add=True, null=False)
    modified_by             = models.ForeignKey(Users, related_name='pull_modified_by')
    modified_ts             = models.DateTimeField(auto_now=True, null=False)
    items                   = ArrayField(models.UUIDField(null=False, blank=False))
    
    class Meta:
        ordering = ['start_dt']
    # End class Meta
# End class Pulls

