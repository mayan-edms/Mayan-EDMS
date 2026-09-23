<#
.SYNOPSIS
    Fibex EDMS Local Development Manager (Podman & Docker compatible)

.DESCRIPTION
    Helper script to run and manage Fibex EDMS in local development with live reload.
    Supports both Podman and Docker Desktop seamlessly.

.EXAMPLE
    .\dev.ps1 start       # Starts dev server with live reload
    .\dev.ps1 stop        # Stops the running dev container
    .\dev.ps1 logs        # Follows container logs (default: last 100 lines)
    .\dev.ps1 logs 50     # Follows container logs from last 50 lines
    .\dev.ps1 logs all    # Follows entire container log history
    .\dev.ps1 shell       # Opens a bash prompt in the dev container
    .\dev.ps1 manage ...  # Runs manage.py commands (e.g. .\dev.ps1 manage check)
    .\dev.ps1 build       # Rebuilds the dev image
#>

param (
    [Parameter(Position = 0)]
    [ValidateSet("start", "stop", "restart", "logs", "shell", "manage", "build", "status")]
    [string]$Action = "start",

    [Parameter(Position = 1, ValueFromRemainingArguments = $true)]
    [string[]]$ExtraArgs
)

$ErrorActionPreference = "Stop"
$ContainerName = "fibex-dev"
$ImageName = "fibex-edms-app:latest"

# Detect engine: prefer Podman if installed and running, otherwise Docker
function Get-ContainerEngine {
    $hasPodman = Get-Command podman -ErrorAction SilentlyContinue
    if ($hasPodman) {
        $podmanState = podman machine inspect 2>$null | ConvertFrom-Json 2>$null
        if ($podmanState -and $podmanState[0].State -eq "running") {
            return "podman"
        }
    }

    $hasDocker = Get-Command docker -ErrorAction SilentlyContinue
    if ($hasDocker) {
        docker info 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            return "docker"
        }
    }

    if ($hasPodman) { return "podman" }
    if ($hasDocker) { return "docker" }
    throw "Neither Podman nor Docker was found or running. Please start Podman or Docker Desktop."
}

$Engine = Get-ContainerEngine

function Build-DevImage {
    Write-Host ">>> Building dev image using $Engine..." -ForegroundColor Cyan
    & $Engine build -f Dockerfile.dev -t $ImageName .
    Write-Host ">>> Build completed: $ImageName" -ForegroundColor Green
}

function Start-DevServer {
    Write-Host ">>> Using container engine: $Engine" -ForegroundColor DarkGray
    Write-Host ">>> Checking if $ContainerName is already running..." -ForegroundColor Cyan

    $running = & $Engine ps --filter "name=^${ContainerName}$" --format "{{.Names}}"
    if ($running -eq $ContainerName) {
        Write-Host ">>> $ContainerName is already running at http://localhost:8000" -ForegroundColor Green
        return
    }

    # Clean up any stopped container with the same name
    & $Engine rm -f $ContainerName 2>$null | Out-Null

    # Check if dev image exists, if not build it
    $imageCheck = & $Engine images -q $ImageName
    if (-not $imageCheck) {
        Write-Host ">>> Image $ImageName not found locally. Building it first..." -ForegroundColor Yellow
        Build-DevImage
    }

    Write-Host ">>> Starting Fibex EDMS Dev Server with Live Reload..." -ForegroundColor Cyan

    if ($Engine -eq "podman") {
        # On Windows with Podman, host networking maps directly to Windows localhost
        podman run -d `
            --name $ContainerName `
            --network host `
            -v ".:/app:z" `
            -w /app `
            -e DJANGO_SETTINGS_MODULE=mayan.settings.development `
            -e MAYAN_MEDIA_ROOT=/app/mayan/media `
            -e PYTHONUNBUFFERED=1 `
            $ImageName `
            python manage.py runserver 0.0.0.0:8000 --settings=mayan.settings.development | Out-Null
    } else {
        # On Docker Desktop, standard port mapping works out of the box
        docker run -d `
            --name $ContainerName `
            -p 8000:8000 `
            -v "${PWD}:/app" `
            -w /app `
            -e DJANGO_SETTINGS_MODULE=mayan.settings.development `
            -e MAYAN_MEDIA_ROOT=/app/mayan/media `
            -e PYTHONUNBUFFERED=1 `
            $ImageName `
            python manage.py runserver 0.0.0.0:8000 --settings=mayan.settings.development | Out-Null
    }

    Write-Host ">>> Container launched. Waiting for server to initialize..." -ForegroundColor Cyan
    
    $ready = $false
    for ($i = 0; $i -lt 60; $i++) {
        Start-Sleep -Seconds 1
        try {
            $resp = Invoke-WebRequest -Uri "http://localhost:8000" -UseBasicParsing -TimeoutSec 2 -ErrorAction SilentlyContinue
            if ($resp.StatusCode -in 200, 302) {
                $ready = $true
                break
            }
        } catch {
            # Still booting
        }
        Write-Host -NoNewline "."
    }
    Write-Host ""

    if ($ready) {
        Write-Host ">>> Fibex EDMS is READY at: http://localhost:8000" -ForegroundColor Green
        Write-Host ">>> Live reload is active! Edit any code in your IDE to trigger reload." -ForegroundColor Green
        Write-Host ">>> Default login: admin / adminpassword" -ForegroundColor Green
    } else {
        Write-Host ">>> Server is still booting. Follow logs with: .\dev.ps1 logs" -ForegroundColor Yellow
    }
}

function Stop-DevServer {
    Write-Host ">>> Stopping $ContainerName using $Engine..." -ForegroundColor Cyan
    & $Engine stop $ContainerName 2>$null | Out-Null
    & $Engine rm $ContainerName 2>$null | Out-Null
    Write-Host ">>> Stopped." -ForegroundColor Green
}

function Show-Logs {
    $lines = if ($ExtraArgs) { $ExtraArgs[0] } else { "100" }
    if ($lines -eq "all") {
        Write-Host ">>> Showing full log history for $ContainerName..." -ForegroundColor DarkGray
        & $Engine logs -f $ContainerName
    } else {
        Write-Host ">>> Showing last $lines lines for $ContainerName (use '.\dev.ps1 logs all' for full history)..." -ForegroundColor DarkGray
        & $Engine logs -f --tail $lines $ContainerName
    }
}

function Enter-Shell {
    & $Engine exec -it $ContainerName /bin/bash
}

function Run-Manage {
    if (-not $ExtraArgs) {
        Write-Host "Usage: .\dev.ps1 manage <command> (e.g. .\dev.ps1 manage check)" -ForegroundColor Yellow
        return
    }
    & $Engine exec -it $ContainerName python manage.py $ExtraArgs
}

function Show-Status {
    & $Engine ps --filter "name=$ContainerName"
}

switch ($Action) {
    "start"   { Start-DevServer }
    "stop"    { Stop-DevServer }
    "restart" { Stop-DevServer; Start-DevServer }
    "logs"    { Show-Logs }
    "shell"   { Enter-Shell }
    "manage"  { Run-Manage }
    "build"   { Build-DevImage }
    "status"  { Show-Status }
}
