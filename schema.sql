-- Consider switching to SQLAlchemy since it is more popular?
drop table if exists users;
create table users (
    id integer primary key autoincrement,
    username text not null,
    password text not null,
    points integer not null
);
insert into users (username, password, points) values ('nufootball', 'sucks', 0);

drop table if exists feedback;
create table feedback (
    id integer primary key autoincrement,
    title text not null,
    text text not null,
    userId integer not null,
    points integer not null,    
    foreign key (userId) REFERENCES users(id)
);