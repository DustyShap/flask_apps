drop table if exists hospitals;
create table hospitals (
  id integer primary key,
  name text not null,
  city text not null,
  state text not null,
  address text not null
);