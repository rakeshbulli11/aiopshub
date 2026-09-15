@echo off
setlocal

set "VERSION=%~1"
set "PREVIOUS_VERSION=%~2"

if "%VERSION%"=="" (
    echo Usage: deploy-with-rollback.bat v1.2.0 v1.1.0
    exit /b 1
)

if "%PREVIOUS_VERSION%"=="" (
    echo Previous version is required.
    echo Usage: deploy-with-rollback.bat v1.2.0 v1.1.0
    exit /b 1
)

echo ==========================================
echo AIOpsHub Deployment
echo ==========================================
echo New version: %VERSION%
echo Previous version: %PREVIOUS_VERSION%
echo.

echo Deploying %VERSION%...

set "BACKEND_VERSION=%VERSION%"

docker compose -f docker-compose.deploy.yml up -d --force-recreate backend

if errorlevel 1 (
    echo.
    echo Deployment command FAILED.
    goto rollback
)

echo.
echo Waiting for application...
timeout /t 5 /nobreak >nul

echo.
echo Running health check...

curl --fail http://localhost:8000/health

if errorlevel 1 (
    echo.
    echo Health check FAILED.
    goto rollback
)

echo.
echo ==========================================
echo Deployment successful
echo ==========================================
docker inspect aiopshub-backend --format "{{.Config.Image}}"

exit /b 0


:rollback

echo.
echo ==========================================
echo Starting automatic rollback
echo ==========================================
echo Rolling back to %PREVIOUS_VERSION%...

set "BACKEND_VERSION=%PREVIOUS_VERSION%"

docker compose -f docker-compose.deploy.yml up -d --force-recreate backend

if errorlevel 1 (
    echo.
    echo ROLLBACK FAILED.
    exit /b 1
)

echo.
echo Waiting for rollback health check...
timeout /t 5 /nobreak >nul

curl --fail http://localhost:8000/health

if errorlevel 1 (
    echo.
    echo ROLLBACK HEALTH CHECK FAILED.
    exit /b 1
)

echo.
echo ==========================================
echo Rollback successful
echo ==========================================
docker inspect aiopshub-backend --format "{{.Config.Image}}"

exit /b 0