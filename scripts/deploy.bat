@echo off
REM Deployment script for Smart Report Assistant (Windows)

setlocal enabledelayedexpansion

REM Configuration
set APP_NAME=smart-report-assistant
set DOCKER_IMAGE=%APP_NAME%
set CONTAINER_NAME=%APP_NAME%-container
set PORT=5000
set HEALTH_CHECK_URL=http://localhost:%PORT%/

REM Function to log messages
:log
echo [%date% %time%] %~1
goto :eof

:error
echo [%date% %time%] ERROR: %~1
goto :eof

REM Check if Docker is running
:check_docker
docker info >nul 2>&1
if errorlevel 1 (
    call :error "Docker is not running. Please start Docker and try again."
    exit /b 1
)
call :log "Docker is running"
goto :eof

REM Build Docker image
:build_image
call :log "Building Docker image..."
docker build -t %DOCKER_IMAGE% .
if errorlevel 1 (
    call :error "Failed to build Docker image"
    exit /b 1
)
call :log "Docker image built successfully"
goto :eof

REM Stop existing container
:stop_container
docker ps -q -f name=%CONTAINER_NAME% >nul 2>&1
if not errorlevel 1 (
    call :log "Stopping existing container..."
    docker stop %CONTAINER_NAME%
    docker rm %CONTAINER_NAME%
    call :log "Existing container stopped and removed"
)
goto :eof

REM Run container
:run_container
call :log "Starting new container..."
docker run -d --name %CONTAINER_NAME% -p %PORT%:5000 --restart unless-stopped %DOCKER_IMAGE%
if errorlevel 1 (
    call :error "Failed to start container"
    exit /b 1
)
call :log "Container started successfully"
goto :eof

REM Health check
:health_check
call :log "Performing health check..."
timeout /t 10 /nobreak >nul

REM Check if container is running
docker ps -q -f name=%CONTAINER_NAME% >nul
if errorlevel 1 (
    call :error "Container failed to start"
    docker logs %CONTAINER_NAME%
    exit /b 1
)

REM Simple health check with curl (if available) or PowerShell
where curl >nul 2>&1
if not errorlevel 1 (
    for /l %%i in (1,1,10) do (
        curl -f -s %HEALTH_CHECK_URL% >nul 2>&1
        if not errorlevel 1 (
            call :log "Application is healthy"
            call :log "Application is available at: %HEALTH_CHECK_URL%"
            goto :eof
        )
        timeout /t 5 /nobreak >nul
    )
) else (
    REM Fallback: just check if container is running
    call :log "Application container is running"
    call :log "Please manually verify at: %HEALTH_CHECK_URL%"
    goto :eof
)

call :error "Health check failed"
docker logs %CONTAINER_NAME%
exit /b 1

REM Main deployment function
:deploy
call :log "Starting deployment of %APP_NAME%..."
call :check_docker
if errorlevel 1 exit /b 1

call :build_image
if errorlevel 1 exit /b 1

call :stop_container
call :run_container
if errorlevel 1 exit /b 1

call :health_check
if errorlevel 1 exit /b 1

call :log "Deployment completed successfully!"
call :log "Application is running at: %HEALTH_CHECK_URL%"
goto :eof

REM Show status
:status
call :log "Checking deployment status..."
docker ps -f name=%CONTAINER_NAME%
goto :eof

REM Main script logic
if "%1"=="" goto :deploy
if "%1"=="deploy" goto :deploy
if "%1"=="status" goto :status
if "%1"=="stop" call :stop_container && goto :eof
if "%1"=="logs" docker logs -f %CONTAINER_NAME% && goto :eof

echo Usage: %0 [deploy^|status^|stop^|logs]
echo.
echo Commands:
echo   deploy   - Deploy the application (default)
echo   status   - Show deployment status
echo   stop     - Stop the application
echo   logs     - Show application logs
exit /b 1

:deploy
call :deploy
goto :eof
