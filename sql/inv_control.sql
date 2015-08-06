-- Postgres
drop database if exists invc_control;
create database invc_control;

drop owned by invcontrol cascade;
drop role invcontrol;

create role invcontrol with login nosuperuser noreplication nocreatedb nocreaterole with encrpyted password 'I am @user !';

alter database invc_control owner to invcontrol;
grant all on database invc_control to invcontrol;

\c invc_control
drop extension if exists "uuid-ossp" cascade;
drop extension if exists "uri" cascade;
drop extension if exists "pgcrypto" cascade;
create extension "uuid-ossp" with schema public;
create extension "uri" with schema public;
create extension "pgcrypto" with schema public;

CREATE OPERATOR CLASS _uuid_ops DEFAULT FOR TYPE _uuid USING gin AS
      OPERATOR 1 &&(anyarray, anyarray),
      OPERATOR 2 @>(anyarray, anyarray),
      OPERATOR 3 <@(anyarray, anyarray),
      OPERATOR 4 =(anyarray, anyarray),
      FUNCTION 1 uuid_cmp(uuid, uuid),
      FUNCTION 2 ginarrayextract(anyarray, internal, internal),
      FUNCTION 3 ginqueryarrayextract(anyarray, internal, smallint, internal, internal, internal, internal),
      FUNCTION 4 ginarrayconsistent(internal, smallint, anyarray, integer, internal, internal, internal, internal),
      STORAGE uuid;

