# local run of the ingestion script for testing purposes
uv run python ingest_data.py \
  --pg-user=root \
  --pg-password=root \
  --pg-host=localhost \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --target-table=yellow_taxi_trips_2021_1 \
  --year=2021 \
  --month=1 \
  --chunksize=100000

# The docker image to ingest data into Postgres, reside on the same ng-network as the Postgres database.
# --pg-host=pgdatabase changed from localhost to pgdatabase which is the name of the Postgres container within the ng-network
docker run --rm -it \
  --network=ng-network \
  taxi_ingest:v001 \
  --pg-user=root \
  --pg-password=root \
  --pg-host=pgdatabase \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --target-table=yellow_taxi_trips_2021_1 \
  --year=2021 \
  --month=1 \
  --chunksize=100000

# Postgres Database docker image created within ng-network. 
# The latter is created using the "docker network create ng-network" command
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  --network=ng-network \
  --name pgdatabase \
  postgres:18

# GUI for Postgres
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=ng-network \
  --name pgadmin \
  dpage/pgadmin4