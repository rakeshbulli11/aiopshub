@echo off

echo Checking AIOpsHub backend health...

curl --fail http://localhost:8000/health

if errorlevel 1 (
    echo.
    echo Health check FAILED.
    exit /b 1
)

echo.
echo Health check PASSED.
exit /b 0