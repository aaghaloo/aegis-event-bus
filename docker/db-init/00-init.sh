#!/bin/bash
set -e                                    # stop on first error
echo "▶︎ Bootstrap Aegis DB …"

# 1. create DB if missing -------------------------------------------------
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
  -c "SELECT 1 FROM pg_database WHERE datname = 'aegis_event_bus'" \
  | grep -q 1 || psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" \
  -c "CREATE DATABASE aegis_event_bus"

# 2. roles (idempotent) ---------------------------------------------------
for ROLE in a0_rw_user a0_ro_user; do
  PW_VAR=${ROLE/a0_/DB_}_PW            # a0_rw_user → DB_rw_user? no: map below
done                                    # (we’ll set explicit SQL instead)

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "aegis_event_bus" <<EOSQL
CREATE EXTENSION IF NOT EXISTS pgcrypto;

DO \$\$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'a0_rw_user') THEN
    CREATE ROLE a0_rw_user LOGIN PASSWORD '${DB_PW}';
  ELSE
    ALTER  ROLE a0_rw_user      PASSWORD '${DB_PW}';
  END IF;

  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'a0_ro_user') THEN
    CREATE ROLE a0_ro_user LOGIN PASSWORD '${DB_RO_PW}';
  ELSE
    ALTER  ROLE a0_ro_user      PASSWORD '${DB_RO_PW}';
  END IF;
END
\$\$;

-- DB & schema privileges -------------------------------------------------
ALTER DATABASE aegis_event_bus OWNER TO a0_rw_user;
GRANT CONNECT   ON DATABASE aegis_event_bus TO a0_ro_user;
GRANT TEMPORARY ON DATABASE aegis_event_bus TO a0_rw_user;

ALTER SCHEMA public OWNER TO a0_rw_user;
GRANT ALL   ON SCHEMA public TO a0_rw_user;
GRANT USAGE ON SCHEMA public TO a0_ro_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT ON TABLES TO a0_ro_user;
EOSQL
