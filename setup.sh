#!/usr/bin/env bash
set -e

echo
echo "🚀 Setting up Obscured-By-Clouds environment..."
echo

# =========================
# Start Postgres & Adminer
# =========================
echo "Starting Postgres and Adminer containers..."
docker compose up -d postgres adminer

# =========================
# Build App Container
# =========================
echo "Building app container..."
docker compose build obc_app

# =========================
# Wait for Postgres readiness
# =========================
echo "Waiting for Postgres to initialise..."
until docker exec obc_postgres pg_isready -U postgres > /dev/null 2>&1; do
    echo "⏳ Postgres not ready yet..."
    sleep 2
done
echo "✅ Postgres is ready!"

# =========================
# Load Database Schema
# =========================
echo "Loading database schema..."
docker exec -i obc_postgres psql -U postgres -d obc_db -f /sql/create_tables.sql

# =========================
# Verify Tables
# =========================
echo "Verifying tables in obc_db..."
docker exec -it obc_postgres psql -U postgres -d obc_db -c "\dt"

echo
echo "🎉 Setup completed!"
echo
echo "Run your CLI app with:"
echo "    docker compose run --rm app"
echo
echo "Access Adminer at:"
echo "    http://localhost:8181 (user: postgres / password: postgres)"
echo

# =========================
# Run App or Exit
# =========================
echo
read -n1 -s -r -p "Press ENTER to launch the app, or ESC to exit..." key
echo
echo
if [[ $key == $'\x1b' ]]; then
    echo
    echo "Exiting setup. You can run the app later with:"
    echo "    docker compose run --rm app"
    exit 0
else
    echo
    echo "Launching CLI app..."
    docker compose run --rm obc_app
fi
