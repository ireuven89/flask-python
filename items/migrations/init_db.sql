create table if not exists schema_history (
    applied_version integer not null
);

insert into schema_history (applied_version) values (0);

create table if not exists items(
     `id` varchar(63) primary key not null,
     `name` varchar(32) not null default '',
     `download_link` varchar(64) not null default '',
     `created_date` timestamp not null default current_timestamp,
     `updated_date` timestamp not null default current_timestamp
);

create table if not exists publishers(
  `id` varchar(63) primary key not null,
  `name` varchar(32) not null default ''
);