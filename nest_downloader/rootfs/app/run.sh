#!/usr/bin/with-contenv bashio
# ==============================================================================
# Home Assistant Add-on: Nest Video Downloader
# Runs the Nest Video Downloader
# ==============================================================================

bashio::log.info "Starting Nest Video Downloader..."

# Get configuration
NEST_EMAIL=$(bashio::config 'nest_email')
NEST_PASSWORD=$(bashio::config 'nest_password')
DOWNLOAD_PATH=$(bashio::config 'download_path')

# Validate credentials are provided
if [[ -z "${NEST_EMAIL}" ]] || [[ -z "${NEST_PASSWORD}" ]]; then
    bashio::log.error "Nest email and password must be configured"
    bashio::exit.nok "Missing required configuration"
fi

bashio::log.info "Configuration loaded successfully"
bashio::log.info "Download path: ${DOWNLOAD_PATH}"

# Create download directory if it doesn't exist
mkdir -p "${DOWNLOAD_PATH}"

bashio::log.info "Nest Video Downloader is ready"

# TODO: Implement actual Nest API integration
# This should include:
# - Authentication with Nest API using provided credentials
# - Discovery of connected cameras
# - Periodic checking for new videos
# - Downloading videos to the specified path
# Currently placeholder code to keep container running
while true; do
    sleep 3600
done
