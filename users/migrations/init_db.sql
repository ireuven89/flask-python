create table if not exists schema_history (
    applied_version integer not null
);

insert into schema_history (applied_version) values (0);

create table if not exists users(
     `id` varchar(63) primary key not null,
     `name` varchar(32),
     `created_date` timestamp not null default current_timestamp,
     `updated_date` timestamp not null default current_timestamp
);