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
python3 main.py
