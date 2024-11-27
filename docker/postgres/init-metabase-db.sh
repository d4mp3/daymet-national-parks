#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  DROP DATABASE IF EXISTS metabase;
  DROP ROLE IF EXISTS metabase;
  CREATE USER metabase WITH PASSWORD 'metabase';
  CREATE DATABASE metabase;
  GRANT ALL PRIVILEGES ON DATABASE metabase TO metabase;
  \c metabase
  \t
  \o /tmp/grant-privs
SELECT 'GRANT SELECT,INSERT,UPDATE,DELETE ON "' || schemaname || '"."' || tablename || '" TO metabase ;'
FROM pg_tables
WHERE tableowner = CURRENT_USER and schemaname = 'public';
  \o
  \i /tmp/grant-privs
EOSQL