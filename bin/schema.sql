drop table if exists courses;
create table courses (
  id integer primary key autoincrement,
  name text not null,
  instructor text not null,
  description text not null
);
