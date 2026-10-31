# Stage 1: install the Python packages into a virtual environment
FROM python:3.12-slim AS builder

# Skip .pyc files and pip's cache to keep the layer small
ENV PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create the virtual environment the runtime stage will copy
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /build

# Copy requirements first so this layer is cached until requirements change
COPY requirements.txt .
RUN pip install -r requirements.txt

# Stage 2: a clean image with only what the app needs to run
FROM python:3.12-slim AS runtime

LABEL org.opencontainers.image.title="ChaiLedger" \
      org.opencontainers.image.description="Transparent weighing and payment records for smallholder tea farmers" \
      org.opencontainers.image.source="https://github.com/chailedger-team/chailedger" \
      org.opencontainers.image.licenses="MIT"

# Log straight to the console, listen on all interfaces, keep the database in /app/data
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    HOST=0.0.0.0 \
    PORT=5000 \
    CHAILEDGER_DATABASE=/app/data/chailedger.db

# Create a non-root user to run the app
RUN groupadd --system --gid 10001 chailedger \
    && useradd --system --uid 10001 --gid chailedger --no-create-home \
       --shell /usr/sbin/nologin chailedger

WORKDIR /app

# Bring in the installed packages from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the app code, owned by root so the app user cannot change it
COPY app/ ./app/
COPY run.py ./

# The data folder is the only place the app user can write
RUN mkdir -p /app/data && chown chailedger:chailedger /app/data

USER chailedger

EXPOSE 5000

# Mark the container unhealthy if /health stops responding
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen('http://127.0.0.1:' + os.environ.get('PORT', '5000') + '/health', timeout=4)" || exit 1

# Serve the app with gunicorn and create the database tables once before the workers start
CMD ["sh", "-c", "exec gunicorn --bind ${HOST}:${PORT} --workers 2 --preload --access-logfile - run:app"]
