create table position
(
    id   uuid         not null
        primary key,
    name varchar(255) not null
        unique
);

alter table position
    owner to postgres;

create table age_range
(
    id          uuid not null
        primary key,
    start_value integer,
    end_value   integer,
    name        varchar(255)
        unique,
    unique (start_value, end_value)
);

alter table age_range
    owner to postgres;

create table completed_passes_percentage_range
(
    id          uuid not null
        primary key,
    start_value real,
    end_value   real,
    name        varchar(255)
        unique,
    unique (start_value, end_value)
);

alter table completed_passes_percentage_range
    owner to postgres;

create table league
(
    id        uuid         not null
        primary key,
    source_id integer      not null
        unique,
    name      varchar(255) not null
);

alter table league
    owner to postgres;

create table team
(
    id        uuid         not null
        primary key,
    source_id integer      not null
        unique,
    name      varchar(255) not null
);

alter table team
    owner to postgres;

create table infractions_by_match_average_range
(
    id          uuid not null
        primary key,
    start_value real,
    end_value   real,
    name        varchar(255)
        unique,
    unique (start_value, end_value)
);

alter table infractions_by_match_average_range
    owner to postgres;

create table goals_frequency_range
(
    id          uuid not null
        primary key,
    start_value real,
    end_value   real,
    name        varchar(255)
);

alter table goals_frequency_range
    owner to postgres;

create table assists_frequency_range
(
    id          uuid not null
        primary key,
    start_value real,
    end_value   real,
    name        varchar(255)
);

alter table assists_frequency_range
    owner to postgres;

create table player_profile
(
    id        uuid    not null
        primary key,
    source_id integer not null
        constraint player_profile_pk
            unique,
    name      varchar(255),
    age       integer,
    nation    varchar(255)
);

alter table player_profile
    owner to postgres;

create table player_fact
(
    id                          uuid not null
        primary key,
    original_id                 integer,
    team_id                     uuid
        references team,
    player_id                   uuid
        references player_profile,
    league_id                   uuid
        references league,
    age_range_id                uuid
        references age_range,
    infractions_avg_range_id    uuid
        references infractions_by_match_average_range,
    goals_frequency_range_id    uuid
                                     references goals_frequency_range
                                         on delete set null,
    assists_frequency_range_id  uuid
                                     references assists_frequency_range
                                         on delete set null,
    yellow_cards                integer,
    red_cards                   integer,
    goals                       integer,
    assists                     integer,
    goals_per_90_min            double precision,
    assists_per_90_min          double precision,
    shots                       integer,
    goals_per_shot              double precision,
    matches_played              integer,
    starting_matches            integer,
    minutes_played              integer,
    completed_passes            integer,
    overall_score               integer,
    completed_passes_percentage double precision,
    goals_per_match             double precision,
    position_id                 uuid
        references position,
    market_value                double precision,
    creation_date               date
);

alter table player_fact
    owner to postgres;

create function digest(text, text) returns bytea
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function digest(text, text) owner to postgres;

create function digest(bytea, text) returns bytea
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function digest(bytea, text) owner to postgres;

create function hmac(text, text, text) returns bytea
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function hmac(text, text, text) owner to postgres;

create function hmac(bytea, bytea, text) returns bytea
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function hmac(bytea, bytea, text) owner to postgres;

create function crypt(text, text) returns text
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function crypt(text, text) owner to postgres;

create function gen_salt(text) returns text
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function gen_salt(text) owner to postgres;

create function gen_salt(text, integer) returns text
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function gen_salt(text, integer) owner to postgres;

create function encrypt(bytea, bytea, text) returns bytea
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function encrypt(bytea, bytea, text) owner to postgres;

create function decrypt(bytea, bytea, text) returns bytea
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function decrypt(bytea, bytea, text) owner to postgres;

create function encrypt_iv(bytea, bytea, bytea, text) returns bytea
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function encrypt_iv(bytea, bytea, bytea, text) owner to postgres;

create function decrypt_iv(bytea, bytea, bytea, text) returns bytea
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function decrypt_iv(bytea, bytea, bytea, text) owner to postgres;

create function gen_random_bytes(integer) returns bytea
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function gen_random_bytes(integer) owner to postgres;

create function gen_random_uuid() returns uuid
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function gen_random_uuid() owner to postgres;

create function pgp_sym_encrypt(text, text) returns bytea
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function pgp_sym_encrypt(text, text) owner to postgres;

create function pgp_sym_encrypt_bytea(bytea, text) returns bytea
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function pgp_sym_encrypt_bytea(bytea, text) owner to postgres;

create function pgp_sym_encrypt(text, text, text) returns bytea
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function pgp_sym_encrypt(text, text, text) owner to postgres;

create function pgp_sym_encrypt_bytea(bytea, text, text) returns bytea
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function pgp_sym_encrypt_bytea(bytea, text, text) owner to postgres;

create function pgp_sym_decrypt(bytea, text) returns text
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function pgp_sym_decrypt(bytea, text) owner to postgres;

create function pgp_sym_decrypt_bytea(bytea, text) returns bytea
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function pgp_sym_decrypt_bytea(bytea, text) owner to postgres;

create function pgp_sym_decrypt(bytea, text, text) returns text
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function pgp_sym_decrypt(bytea, text, text) owner to postgres;

create function pgp_sym_decrypt_bytea(bytea, text, text) returns bytea
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function pgp_sym_decrypt_bytea(bytea, text, text) owner to postgres;

create function pgp_pub_encrypt(text, bytea) returns bytea
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function pgp_pub_encrypt(text, bytea) owner to postgres;

create function pgp_pub_encrypt_bytea(bytea, bytea) returns bytea
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function pgp_pub_encrypt_bytea(bytea, bytea) owner to postgres;

create function pgp_pub_encrypt(text, bytea, text) returns bytea
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function pgp_pub_encrypt(text, bytea, text) owner to postgres;

create function pgp_pub_encrypt_bytea(bytea, bytea, text) returns bytea
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function pgp_pub_encrypt_bytea(bytea, bytea, text) owner to postgres;

create function pgp_pub_decrypt(bytea, bytea) returns text
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function pgp_pub_decrypt(bytea, bytea) owner to postgres;

create function pgp_pub_decrypt_bytea(bytea, bytea) returns bytea
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function pgp_pub_decrypt_bytea(bytea, bytea) owner to postgres;

create function pgp_pub_decrypt(bytea, bytea, text) returns text
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function pgp_pub_decrypt(bytea, bytea, text) owner to postgres;

create function pgp_pub_decrypt_bytea(bytea, bytea, text) returns bytea
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function pgp_pub_decrypt_bytea(bytea, bytea, text) owner to postgres;

create function pgp_pub_decrypt(bytea, bytea, text, text) returns text
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function pgp_pub_decrypt(bytea, bytea, text, text) owner to postgres;

create function pgp_pub_decrypt_bytea(bytea, bytea, text, text) returns bytea
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function pgp_pub_decrypt_bytea(bytea, bytea, text, text) owner to postgres;

create function pgp_key_id(bytea) returns text
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function pgp_key_id(bytea) owner to postgres;

create function armor(bytea) returns text
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function armor(bytea) owner to postgres;

create function armor(bytea, text[], text[]) returns text
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function armor(bytea, text[], text[]) owner to postgres;

create function dearmor(text) returns bytea
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function dearmor(text) owner to postgres;

create function pgp_armor_headers(text, out key text, out value text) returns setof setof record
    immutable
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;

$$;

alter function pgp_armor_headers(text, out text, out text) owner to postgres;

