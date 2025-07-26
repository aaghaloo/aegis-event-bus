-- docker/db-init/00-init.sql
-- Bootstrap the database + RW/RO roles.
-- Passwords come from container-env (DB_PW / DB_RO_PW), **not** hard-coded.

\echo '▶︎ Reading passwords from environment …'
\set db_pw      :'DB_PW'
\set db_ro_pw   :'DB_RO_PW'

-------------------------------------------------------------------------------
-- 1. create database if missing ----------------------------------------------
DO
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'aegis_event_bus') THEN
        CREATE DATABASE aegis_event_bus;
    END IF;
END
$$;

-------------------------------------------------------------------------------
-- 2. connect into the target DB ----------------------------------------------
\connect aegis_event_bus

-------------------------------------------------------------------------------
-- 3. pgcrypto (needed later for UUID / hashes etc.) ---------------------------
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-------------------------------------------------------------------------------
-- 4. create / amend roles -----------------------------------------------------
DO
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'a0_rw_user') THEN
        EXECUTE format($f$CREATE ROLE a0_rw_user LOGIN PASSWORD %L$f$, :'db_pw');
    ELSE
        EXECUTE format($f$ALTER  ROLE a0_rw_user      PASSWORD %L$f$, :'db_pw');
    END IF;

    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'a0_ro_user') THEN
        EXECUTE format($f$CREATE ROLE a0_ro_user LOGIN PASSWORD %L$f$, :'db_ro_pw');
    ELSE
        EXECUTE format($f$ALTER  ROLE a0_ro_user      PASSWORD %L$f$, :'db_ro_pw');
    END IF;
END
$$;

-------------------------------------------------------------------------------
-- 5. DB-level privileges ------------------------------------------------------
ALTER DATABASE aegis_event_bus OWNER TO a0_rw_user;

GRANT CONNECT    ON DATABASE aegis_event_bus TO a0_ro_user;
GRANT TEMPORARY  ON DATABASE aegis_event_bus TO a0_rw_user;

-------------------------------------------------------------------------------
-- 6. schema privileges --------------------------------------------------------
ALTER SCHEMA public OWNER TO a0_rw_user;

GRANT ALL     ON  SCHEMA public TO a0_rw_user;
GRANT USAGE   ON  SCHEMA public TO a0_ro_user;

-- future tables: RO can SELECT, RW owns everything
ALTER DEFAULT PRIVILEGES IN SCHEMA public
        GRANT SELECT ON TABLES TO a0_ro_user;
