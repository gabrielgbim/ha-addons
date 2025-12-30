#!/usr/bin/with-contenv bashio
# ==============================================================================
# Home Assistant Add-on: Nest Video Downloader
# Runs the Nest Video Downloader
# ==============================================================================

bashio::log.info "Starting Nest Video Downloader..."

# Get configuration
export BASE_PATH=$(bashio::config 'BASE_PATH')
export GOOGLE_USERNAME=$(bashio::config 'GOOGLE_USERNAME')
export GOOGLE_MASTER_TOKEN=$(bashio::config 'GOOGLE_MASTER_TOKEN')
export LOCAL_TIMEZONE=$(bashio::config 'LOCAL_TIMEZONE')
export REFRESH_INTERVAL=$(bashio::config 'REFRESH_INTERVAL')

# Validate required configuration
if [[ -z "${GOOGLE_USERNAME}" ]] || [[ -z "${GOOGLE_MASTER_TOKEN}" ]]; then
    bashio::log.error "Google username and master token must be configured"
    bashio::exit.nok "Missing required configuration"
fi

bashio::log.info "Configuration loaded successfully"
bashio::log.info "Base path: ${BASE_PATH}"
bashio::log.info "Local timezone: ${LOCAL_TIMEZONE}"
bashio::log.info "Refresh interval: ${REFRESH_INTERVAL} minutes"

# Start Python application
bashio::log.info "Starting Python application..."
cd /app || bashio::exit.nok "Failed to change to /app directory"

# Check if main.py exists
if [ ! -f "main.py" ]; then
    bashio::exit.nok "main.py not found in /app directory"
fi

# Check Python version
bashio::log.info "Python version: $(python3 --version)"

# List files for debugging
bashio::log.info "Files in /app: $(ls -la /app)"

# Try to import modules first to catch import errors
bashio::log.info "Testing Python imports..."
python3 -u -c "import sys; print('Python import test'); sys.stdout.flush()" 2>&1

# Test if we can import the main modules
bashio::log.info "Testing main.py imports..."
python3 -u -c "
import sys
sys.path.insert(0, '/app')
try:
    print('Testing auth...', flush=True)
    import auth
    print('Testing models...', flush=True)
    import models
    print('Testing nest_device...', flush=True)
    import nest_device
    print('Testing downloader...', flush=True)
    import downloader
    print('All imports successful!', flush=True)
except Exception as e:
    print(f'Import error: {e}', flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
" 2>&1

# Run the application with stderr also unbuffered
bashio::log.info "Executing main.py..."

# Test if main.py even starts
bashio::log.info "Testing main.py execution..."
python3 -u -c "
import sys
sys.path.insert(0, '/app')
print('About to run main.py...', flush=True)
exec(open('/app/main.py').read())
" 2>&1

bashio::log.info "main.py exited"
