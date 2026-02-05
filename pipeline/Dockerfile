FROM python:3.13.11-slim

# Copy the uv executable from the astral-sh/uv image to /bin/ for package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code

# Prepend the virtual environment's bin directory to PATH so Python commands automatically use the venv
# This eliminates the need to use 'uv run' in the entrypoint
ENV PATH="/code/.venv/bin:$PATH"

COPY pyproject.toml .python-version uv.lock green_tripdata_2025-11.parquet ./

# install dependencies from uv.lock
RUN uv sync --locked

COPY ingest_datasets.py .

ENTRYPOINT ["python", "ingest_datasets.py"]