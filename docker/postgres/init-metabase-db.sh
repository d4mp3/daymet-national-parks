#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  DROP DATABASE IF EXISTS metabase;
  DROP ROLE IF EXISTS metabase;
  CREATE USER metabase WITH PASSWORD 'metabase';
  GRANT CREATE ON SCHEMA public TO metabase;
  ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT UPDATE, INSERT, SELECT, DELETE, CREATE ON TABLES TO metabase;
  CREATE DATABASE metabase;
  ALTER DATABASE metabase owner to metabase;
