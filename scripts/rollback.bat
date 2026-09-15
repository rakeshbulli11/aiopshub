@echo off
setlocal

set "ROLLBACK_VERSION=%~1"

if "%ROLLBACK_VERSION%"=="" (
    echo Usage: rollback.bat v1.1.0
    exit /b 1
)

echo Rolling back AIOpsHub to %ROLLBACK_VERSION%...

set "BACKEND_VERSION=%ROLLBACK_VERSION%"

docker compose up -d --force-recreate backend

if errorlevel 1 (
    echo Rollback failed.
    exit /b 1
)

echo Waiting for backend health...

timeout /t 5 /nobreak >nul

curl --fail http://localhost:8000/health

if errorlevel 1 (
    echo Health check failed after rollback.
    exit /b 1
)

echo Rollback completed successfully.
echo Running version:
docker inspect aiopshub-backend --format "{{.Config.Image}}"

endlocal