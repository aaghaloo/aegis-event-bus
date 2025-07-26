-- docker/db-init/00-init.sql
-- Bootstrap: database + RW / RO roles + extension + privileges
-----------------------------------------------------------------
-- 1. create the database if it is missing ----------------------
DO
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'aegis_event_bus')
    THEN
        CREATE DATABASE aegis_event_bus;
    END IF;
END
$$;

-----------------------------------------------------------------
-- 2. switch into the fresh DB ----------------------------------
\connect aegis_event_bus

-----------------------------------------------------------------
-- 3. make sure pgcrypto is installed ---------------------------
-- (runs as super-user “postgres”, so it always succeeds)
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-----------------------------------------------------------------
-- 4. roles ------------------------------------------------------
DO
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'a0_rw_user')
    THEN
        CREATE ROLE a0_rw_user LOGIN PASSWORD 'change_me_rw';
    END IF;

    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'a0_ro_user')
    THEN
        CREATE ROLE a0_ro_user LOGIN PASSWORD 'change_me_ro';
    END IF;
END
$$;

-----------------------------------------------------------------
-- 5. database-level privileges ---------------------------------
-- a0_rw_user is made *owner*; that automatically allows CREATE,
-- ALTER and extension management in this DB.
ALTER DATABASE aegis_event_bus OWNER TO a0_rw_user;

GRANT CONNECT          ON DATABASE aegis_event_bus TO a0_ro_user;
GRANT TEMPORARY        ON DATABASE aegis_event_bus TO a0_rw_user;

-----------------------------------------------------------------
-- 6. schema-level privileges -----------------------------------
ALTER SCHEMA public OWNER TO a0_rw_user;
GRANT  ALL PRIVILEGES ON  SCHEMA public TO a0_rw_user;
GRANT  USAGE          ON  SCHEMA public TO a0_ro_user;

-- any *future* tables: RW owns, RO can SELECT
ALTER DEFAULT PRIVILEGES IN SCHEMA public
        GRANT SELECT ON TABLES TO a0_ro_user;
