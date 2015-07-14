-- Postgres
drop extension if exists "uuid-ossp" cascade;
drop extension if exists "uri" cascade;
create extension "uuid-ossp" with schema public;
create extension "uri" with schema public;

drop database if exists invc_control;
create database invc_control;

drop owned by setup_user, invc_users, invc_admins cascade;
drop role setup_user;
drop role invc_users;
drop role invc_admins;

create role invc_users with nologin nosuperuser noreplication nocreatedb nocreaterole;
create role invc_admins with nologin createrole createdb replication;

alter database invc_control owner to invc_admins;
grant connect on database invc_control to invc_users, invc_admins;
grant temp on database invc_control to invc_users, invc_admins;


\c invc_control
create schema invc_control authorization invc_admins;
grant usage on schema invc_control to invc_users invc_admins;
grant create on schema invc_control to invc_admins;


set search_path = invc_control, public;


drop table if exists invc_control.states cascade;
create table if not exists invc_control.states (
    abbr                char(2) not null primary key,
    name                text not null
);

alter table invc_control.states owner to invc_admins;

begin;
insert into invc_control.states (abbr, name)
values ('AL', 'Alabama'),
       ('AK', 'Alaska'),
       ('AZ', 'Arizona'),
       ('AR', 'Arkansas'),
       ('CA', 'California'),
       ('CO', 'Colorado'),
       ('CT', 'Connecticut'),
       ('DE', 'Delaware'),
       ('DC', 'District of Columbia'),
       ('FL', 'Florida'),
       ('GA', 'Georgia'),
       ('HI', 'Hawaii'),
       ('ID', 'Idaho'),
       ('IL', 'Illinois'),
       ('IN', 'Indiana'),
       ('IA', 'Iowa'),
       ('KS', 'Kansas'),
       ('KY', 'Kentucky'),
       ('LA', 'Louisiana'),
       ('ME', 'Maine'),
       ('MD', 'Maryland'),
       ('MA', 'Massachusetts'),
       ('MI', 'Michigan'),
       ('MN', 'Minnesota'),
       ('MS', 'Mississippi'),
       ('MO', 'Missouri'),
       ('MT', 'Montana'),
       ('NE', 'Nebraska'),
       ('NV', 'Nevada'),
       ('NH', 'New Hampshire'),
       ('NJ', 'New Jersey'),
       ('NM', 'New Mexico'),
       ('NY', 'New York'),
       ('NC', 'North Carolina'),
       ('ND', 'North Dakota'),
       ('OH', 'Ohio'),
       ('OK', 'Oklahoma'),
       ('OR', 'Oregon'),
       ('PA', 'Pennsylvania'),
       ('RI', 'Rhode Island'),
       ('SC', 'South Carolina'),
       ('SD', 'South Dakota'),
       ('TN', 'Tennessee'),
       ('TX', 'Texas'),
       ('UT', 'Utah'),
       ('VT', 'Vermont'),
       ('VA', 'Virginia'),
       ('WA', 'Washington'),
       ('WV', 'West Virginia'),
       ('WI', 'Wisconsin'),
       ('WY', 'Wyoming'),
       ('AS', 'American Samoa'),
       ('GU', 'Guam'),
       ('MP', 'Northern Mariana Islands'),
       ('PR', 'Puerto Rico'),
       ('VI', 'Virgin Islands'),
       ('FM', 'Federated States of Micronesia'),
       ('MH', 'Marshall Islands'),
       ('PW', 'Palau'),
       ('AA', 'U.S. Armed Forces – Americas[4]'),
       ('AE', 'U.S. Armed Forces – Europe[5]'),
       ('AP', 'U.S. Armed Forces – Pacific[6]'),
       ('CM', 'Northern Mariana Islands'),
       ('CZ', 'Panama Canal Zone'),
       ('NB', 'Nebraska'),
       ('PI', 'Philippine Islands'),
       ('TT', 'Trust Territory of the Pacific Islands');
commit;


drop table if exists invc_control.users cascade;
create table if not exists invc_control.users (
    id                  uuid not null default uuid_generate_v4() primary key,
    userid              text not null,
    password            text not null,
    surname             text not null,
    midname             text,
    forename            text not null,
    address1            text not null,
    address2            text,
    city                text not null,
    state               char(2) not null references invc_control.states(abbr),
    zipcode             text not null,
    telno               text,
    telno_type          text check ( telno_type = any (array['land-line', 'mobile', 'fax', 'other']) ),
    email               text,
    active              boolean not null default true,
    is_admin            boolean not null default false,
    created_ts          timestamp not null default current_timestamp,
    created_by          uuid not null references invc_control.users(id),
    modified_ts         timestamp not null default current_timestamp,
    modified_by         uuid not null references invc_control.users(id)
);

alter table invc_control.users owner to invc_admins;

create unique index users_uix_01 on invc_control.invc_control.users(userid);


drop table if exists invc_control.value_types cascade;
create table if not exists invc_control.value_types (
    type_name               varchar(50) not null primary key,
    type_desc               text,
    created_ts          timestamp not null default current_timestamp,
    created_by          uuid not null references invc_control.users(id),
    modified_ts         timestamp not null default current_timestamp,
    modified_by         uuid not null references invc_control.users(id)
);

alter table invc_control.value_types owner to invc_admins;

begin;
insert into invc_control.value_types (type_name, type_desc, created_by, modified_by)
values ('DECIMAL', 'Decimal (0.0)', 0, 0),
       ('INTEGER', 'Integer', 0, 0),
       ('TEXT', 'Text', 0, 0),
       ('BINARY', 'Binary', 0, 0);
commit;


drop table if exists invc_control.config cascade;
create table if not exists invc_control.config (
    key                 text not null primary key,
    value               text not null,
    value_type          varchar(50) not null references invc_control.value_types(type_name),
    created_ts          timestamp not null default current_timestamp,
    created_by          uuid not null references invc_control.users(id),
    modified_ts         timestamp not null default current_timestamp,
    modified_by         uuid not null references invc_control.users(id)
);

alter table invc_control.config owner to invc_admins;

begin;
insert into invc_control.config(key, value, value_type, created_by, modified_by)
values ('COMPANY_LOGO', '', 'BINARY', 0, 0);
commit;


drop table if exists invc_control.warehouses cascade;
create table if not exists invc_control.warehouses (
    id                  uuid not null default uuid_generate_v4() primary key,
    name                text not null,
    description         text,
    address1            text not null,
    address2            text,
    city                text not null,
    state               char(2) not null references invc_control.states(abbr),
    zipcode             text not null,
    telno               text,
    telno_type          text check ( telno_type = any (array['land-line', 'mobile', 'fax', 'other']) ),
    email               text,
    map_url             url,
    start_dt            date,
    end_dt              date,
    created_ts          timestamp not null default current_timestamp,
    created_by          uuid not null references invc_control.users(id),
    modified_ts         timestamp not null default current_timestamp,
    modified_by         uuid not null references invc_control.users(id)
);

alter table invc_control.warehouses owner to invc_admins;

create unique index warehouse_uix_01 on invc_control.warehouses (name);


drop table if exists invc_control.warehouse_areas cascade;
create table if not exists invc_control.warehouse_areas (
    id                  uuid not null default uuid_generate_v4() primary key,
    name                text not null,
    description         text,
    warehouse_id        uuid not null references invc_control.warehouses(id),
    created_ts          timestamp not null default current_timestamp,
    created_by          uuid not null references invc_control.users(id),
    modified_ts         timestamp not null default current_timestamp,
    modified_by         uuid not null references invc_control.users(id)
);

alter table invc_control.warehouse_areas owner to invc_admins;

create unique index warehouse_area_uix_01 on invc_control.warehouse_areas (name);


drop table if exists invc_control.area_racks cascade;
create table if not exists invc_control.area_racks (
    id                  uuid not null default uuid_generate_v4() primary key,
    name                text not null,
    description         text,
    warehouse_area_id   uuid not null references invc_control.warehouse_areas(id),
    created_ts          timestamp not null default current_timestamp,
    created_by          uuid not null references invc_control.users(id),
    modified_ts         timestamp not null default current_timestamp,
    modified_by         uuid not null references invc_control.users(id)
);

alter table invc_control.area_racks owner to invc_admins;

create unique index area_rack_uix_01 on invc_control.area_racks (name);


drop index if exists invc_control.rack_shelves;
create table if not exists invc_control.rack_shelves (
    id                  uuid not null default uuid_generate_v4() primary key,
    name                text not null,
    description         text,
    area_rack_id        uuid not null references invc_control.area_racks(id),
    created_ts          timestamp not null default current_timestamp,
    created_by          uuid not null references invc_control.users(id),
    modified_ts         timestamp not null default current_timestamp,
    modified_by         uuid not null references invc_control.users(id)
);

alter table invc_control.rack_shelves owner to invc_admins;

create unique index rack_shelf_uix_01 on invc_control.rack_shelves (name);


drop table if exists invc_control.items cascade;
create table if not exists invc_control.items (
    id                      uuid not null default uuid_generate_v4() primary key,
    name                    text not null,
    description             text,
    tags                    text[],
    image                   bytea,
    height                  float,
    width                   float,
    depth                   float,
    unit_measure            text not null default 'inches' check (unit_measure = any (array['inches', 'feet', 'centimeters', 'meters'])),
    current_location_id     uuid not null,
    current_location_type   text not null default 'warehouse' check (current_location_type = any (array['warehouse', 'in-transit', 'on-contract'])),
    active                  boolean not null default true,
    created_ts          timestamp not null default current_timestamp,
    created_by          uuid not null references invc_control.users(id),
    modified_ts         timestamp not null default current_timestamp,
    modified_by         uuid not null references invc_control.users(id)
);

alter table invc_control.items owner to invc_admins;

create index item_ix_01 on invc_control.items using gin (tags);


drop table if exists invc_control.contracts cascade;
create table if not exists invc_control.contracts (
    id                      uuid not null default uuid_generate_v4() primary key,
    name                    varchar(256) not null,
    description             text,
    start_dt                date not null,
    end_dt                  date,
    dropoff_dt              date,
    pickup_dt               date,
    address1            text not null,
    address2            text,
    city                text not null,
    state               char(2) not null references invc_control.states(abbr),
    zipcode             text not null,
    telno               text,
    telno_type          text check ( telno_type = any (array['land-line', 'mobile', 'fax', 'other']) ),
    email               text,
    items               uuid[], -- items reserved/used for the contract
    created_ts          timestamp not null default current_timestamp,
    created_by          uuid not null references invc_control.users(id),
    modified_ts         timestamp not null default current_timestamp,
    modified_by         uuid not null references invc_control.users(id)
);

alter table invc_control.contracts owner to invc_admins;


drop table if exists invc_control.warehouse_item_location cascade;
create table if not exists invc_control.warehouse_item_location (
    id                  uuid not null default uuid_generate_v4() primary key,
    warehouse_id        uuid references invc_control.warehouses(id),
    warehouse_area_id   uuid references invc_control.warehouse_areas(id),
    area_rack_id        uuid references invc_control.area_racks(id),
    rack_shelf_id       uuid references invc_control.rack_shelves(id),
    item_id             uuid not null references invc_control.items(id),
    created_ts          timestamp not null default current_timestamp,
    created_by          uuid not null references invc_control.users(id),
    modified_ts         timestamp not null default current_timestamp,
    modified_by         uuid not null references invc_control.users(id)
);

alter table invc_control.warehouse_item_location owner to invc_admins;


grant select, insert, update, delete on all tables in schema invc_control to invc_users;
grant all on all tables in schema invc_control to invc_admins;
grant all on all sequences in schema invc_control to invc_users invc_admins;


create role invadmin with login inherit encrypted password '{ADMIN_ENC_PASSWD}' in role invc_admins;
create role invuser with login inherit encrypted password '{USER_ENC_PASSWD}' in role invc_users;

insert into users (id, userid, password, surname, forename, address1, city, state, zipcode, created_by, modified_by)
values (uuid_nil(), 'root', '{ROOT_PASSWORD}', 'Admin', 'root', 'localhost', 'pty1', 'DC', '00000', uuid_nil(), uuid_nil());

