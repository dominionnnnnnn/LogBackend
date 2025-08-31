FROM python:3.13.3-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Work inside /app/src since manage.py and config/ live there
WORKDIR /app/src

# Install system dependencies
RUN apt-get update && apt-get install -y curl build-essential libpq-dev

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy requirements and install
COPY src/requirements.txt /app/src/
RUN uv pip install -r requirements.txt --system

# Copy project files
COPY src/ /app/src/

# Collect static later via Render Pre-Deploy command, not here

# Run with Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
