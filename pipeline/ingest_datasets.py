#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from tqdm.auto import tqdm
from sqlalchemy import create_engine
import pyarrow.parquet as pq

# --- Database configuration ---
PG_USER = "root"
PG_PASSWORD = "root"
PG_HOST = "pgdatabase"
PG_PORT = 5432
PG_DB = "ny_taxi"

# --- Table names ---
YELLOW_TABLE = "yellow_taxi_trips_2021_01"
GREEN_TABLE = "green_taxi_trips_2025_11"
ZONES_TABLE = "zones"

# --- CSV & Parquet URLs ---
YELLOW_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
# GREEN_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
GREEN_FILE = "green_tripdata_2025-11.parquet"

TAXI_ZONES_URL = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"

# --- CSV dtypes and parsing ---
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

CHUNKSIZE = 100000


def write_zones_table(engine):
    df_zones = pd.read_csv(TAXI_ZONES_URL)
    df_zones.to_sql(ZONES_TABLE, engine, if_exists="replace")
    with engine.connect() as conn:
        conn.commit()
    print(f"{ZONES_TABLE} table ingested.")


def ingest_csv(engine, url, table_name):
    print(f"Ingesting CSV: {url} -> {table_name}")
    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=CHUNKSIZE
    )

    first = True
    for df_chunk in tqdm(df_iter, desc=f"Ingesting {table_name}"):
        if first:
            df_chunk.head(0).to_sql(table_name, engine, if_exists="replace")
            first = False
        df_chunk.to_sql(table_name, engine, if_exists="append")
    print(f"{table_name} ingestion complete.")


def ingest_parquet(engine, url, table_name):
    print(f"Ingesting Parquet: {url} -> {table_name}")
    # Read parquet in batches using pyarrow
    table = pq.read_table(url)
    n_rows = table.num_rows
    batch_size = 100_000
    batches = (n_rows + batch_size - 1) // batch_size

    first = True
    for i in tqdm(range(batches), desc=f"Ingesting {table_name}"):
        start = i * batch_size
        end = min((i + 1) * batch_size, n_rows)
        batch_df = table.slice(start, end - start).to_pandas()
        if first:
            batch_df.head(0).to_sql(table_name, engine, if_exists="replace")
            first = False
        batch_df.to_sql(table_name, engine, if_exists="append")
    print(f"{table_name} ingestion complete.")


def main():
    engine = create_engine(f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}")

    # Ingest zones
    write_zones_table(engine)

    # Ingest yellow taxi CSV
    ingest_csv(engine, YELLOW_URL, YELLOW_TABLE)

    # Ingest green taxi Parquet
    ingest_parquet(engine, GREEN_FILE, GREEN_TABLE)


if __name__ == "__main__":
    main()
