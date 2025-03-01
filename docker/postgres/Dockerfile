FROM postgres:15-alpine

COPY init-metabase-db.sh /docker-entrypoint-initdb.d/init-metabase-db.sh

RUN chmod +x /docker-entrypoint-initdb.d/init-metabase-db.sh

EXPOSE 5432
