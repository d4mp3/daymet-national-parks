#!/bin/bash
set -e

echo "Checking if Metabase database exists..."
DB_EXISTS=$(psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "SELECT 1 FROM pg_database WHERE datname='metabase'")

if [ "$DB_EXISTS" = "1" ]; then
  echo "Metabase database already exists. Skipping initialization."
else
  echo "Creating Metabase database..."
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER metabase WITH PASSWORD 'metabase';
    CREATE DATABASE metabase;
    ALTER DATABASE metabase OWNER TO metabase;
    GRANT ALL PRIVILEGES ON DATABASE metabase TO metabase;
EOSQL
  echo "Metabase database created successfully."
fi
