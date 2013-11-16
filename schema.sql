drop table if exists users;
create table users (
    id integer primary key autoincrement,
    username text not null,
    password text not null,
    points integer not null
);
insert into users (username, password, points) values ('dan', 'immarried', 0);

drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);