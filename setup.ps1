# setup.ps1
# Developer-friendly one-click setup for Windows
$ErrorActionPreference = "Stop"

Write-Host "🚀 Setting up Obscured-By-Clouds environment..." -ForegroundColor Cyan
Write-Host ""

# =========================
# Start Postgres & Adminer
# =========================
Write-Host "Starting Postgres and Adminer containers..."
docker compose up -d postgres adminer

# =========================
# Build App Container
# =========================
Write-Host "Building app container..."
docker compose build obc_app

# =========================
# Wait for Postgres readiness
# =========================
Write-Host "Waiting for Postgres to initialise..."
do {
    Start-Sleep -Seconds 2
    $status = docker exec obc_postgres pg_isready -U postgres 2>$null
} until ($status -eq 0)
Write-Host "✅ Postgres is ready!"

# =========================
# Load Database Schema
# =========================
Write-Host "Loading database schema..."
docker exec -i obc_postgres psql -U postgres -d obc_db -f /sql/create_tables.sql

# =========================
# Verify Tables
# =========================
Write-Host "Verifying tables in obc_db..."
docker exec -it obc_postgres psql -U postgres -d obc_db -c "\dt"

# =========================
# Launch App Prompt
# =========================
Write-Host ""
Write-Host "Press ENTER to launch the CLI app (source/app.py), or ESC to exit..."
$host.UI.RawUI.FlushInputBuffer()
$key = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

if ($key.VirtualKeyCode -eq 27) {   # ESC key
    Write-Host ""
    Write-Host "Exiting setup. You can run the app later with: docker compose run --rm app"
    exit
} else {
    Write-Host ""
    Write-Host "Launching CLI app..."
    docker compose run --rm obc_app
}

