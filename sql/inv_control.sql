-- Postgres
drop database if exists invc_control;
create database invc_control;

drop owned by invc_users, invc_admins cascade;
drop role invuser;
drop role invadmin;
drop role invc_users;
drop role invc_admins;

create role invc_users with nologin nosuperuser noreplication nocreatedb nocreaterole;
create role invc_admins with nologin createrole createdb replication;

alter database invc_control owner to invc_admins;
grant connect on database invc_control to invc_users, invc_admins;
grant temp on database invc_control to invc_users, invc_admins;


\c invc_control
drop extension if exists "uuid-ossp" cascade;
drop extension if exists "uri" cascade;
create extension "uuid-ossp" with schema public;
create extension "uri" with schema public;

create schema invc_control authorization invc_admins;
grant usage on schema invc_control to invc_users, invc_admins;
grant create on schema invc_control to invc_admins;


set search_path = invc_control, public, pg_catalog;


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
    id                  uuid not null default public.uuid_generate_v4() primary key,
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
    modified_by         uuid not null references invc_control.users(id),
    image               bytea
);

alter table invc_control.users owner to invc_admins;

create unique index users_uix_01 on invc_control.invc_control.users(userid);


drop table if exists invc_control.warehouses cascade;
create table if not exists invc_control.warehouses (
    id                  uuid not null default public.uuid_generate_v4() primary key,
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
    map_url             uri,
    height                  float,
    width                   float,
    depth                   float,
    unit_measure            text not null default 'inches' check (unit_measure = any (array['inches', 'feet', 'centimeters', 'meters'])),
    start_dt            date,
    end_dt              date,
    created_ts          timestamp not null default current_timestamp,
    created_by          uuid not null references invc_control.users(id),
    modified_ts         timestamp not null default current_timestamp,
    modified_by         uuid not null references invc_control.users(id),
    image               bytea
);

alter table invc_control.warehouses owner to invc_admins;

create unique index warehouse_uix_01 on invc_control.warehouses (name);


drop table if exists invc_control.warehouse_containers cascade;
create table if not exists invc_control.warehouse_containers (
    id                  uuid not null default public.uuid_generate_v4() primary key,
    warehouse_id        uuid not null references invc_control.warehouses(id),
    container_parent_id uuid not null references invc_control.warehouse_containers(id),
    container_type      text not null check (container_type = any(array['warehouse', 'area', 'rack', 'shelf', 'bin', 'section'])),
    container_name      text not null,
    description         text,
    height                  float,
    width                   float,
    depth                   float,
    unit_measure            text not null default 'inches' check (unit_measure = any (array['inches', 'feet', 'centimeters', 'meters'])),
    created_ts          timestamp not null default current_timestamp,
    created_by          uuid not null references invc_control.users(id),
    modified_ts         timestamp not null default current_timestamp,
    modified_by         uuid not null references invc_control.users(id),
    image               bytea
);

alter table invc_control.warehouse_containers owner to invc_admins;

create unique index warehouse_containers_uix_01 on invc_control.warehouse_containers (container_name);
create index warehouse_containers_ix_01 on invc_control.warehouse_containers (warehouse_id);
create index warehouse_containers_ix_02 on invc_control.warehouse_containers (container_parent_id);


drop table if exists invc_control.items cascade;
create table if not exists invc_control.items (
    id                      uuid not null default public.uuid_generate_v4() primary key,
    name                    text not null,
    description             text,
    tags                    text[],
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
    modified_by         uuid not null references invc_control.users(id),
    image               bytea
);

alter table invc_control.items owner to invc_admins;

create index item_ix_01 on invc_control.items using gin (tags);


drop table if exists invc_control.contracts cascade;
create table if not exists invc_control.contracts (
    id                      uuid not null default public.uuid_generate_v4() primary key,
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


grant select, insert, update, delete on all tables in schema invc_control to invc_users;
grant all on all tables in schema invc_control to invc_admins;
grant all on all sequences in schema invc_control to invc_users, invc_admins;


create role invadmin with login inherit encrypted password 'invadmin01' in role invc_admins;
create role invuser with login inherit encrypted password 'invuser01' in role invc_users;

insert into users (id, userid, password, surname, forename, address1, city, state, zipcode, created_by, modified_by)
values (public.uuid_nil(), 'root', '$admin01', 'Admin', 'root', 'localhost', 'pty1', 'DC', '00000', public.uuid_nil(), public.uuid_nil());

