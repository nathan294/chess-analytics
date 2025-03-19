# Use an official Python runtime as a parent image
FROM python:3.13-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.6.8 /uv /bin/uv

# Install Git
RUN apt-get update && apt-get install -y git

# Install locales and dependencies for locale generation
RUN apt-get update && \
    apt-get install -y locales && \
    rm -rf /var/lib/apt/lists/*

# Generate the 'fr_FR.UTF-8' locale
RUN echo "fr_FR.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen fr_FR.UTF-8 && \
    update-locale LANG=fr_FR.UTF-8

# Set environment variables for locale
ENV LANG fr_FR.UTF-8
ENV LANGUAGE fr_FR:fr
ENV LC_ALL fr_FR.UTF-8

# Copy the project into the image
ADD . /app
WORKDIR /app

# Install the dependencies using UV
# Sync the project into a new environment
RUN uv sync

# Use the virtual environment automatically
ENV VIRTUAL_ENV=/app/.venv
# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# CMD ["gunicorn","src.chess_analytics.app:server","--bind",":8050"]