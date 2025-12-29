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

bashio::log.info "Configuration loaded"
bashio::log.info "Download path: ${DOWNLOAD_PATH}"

# Create download directory if it doesn't exist
mkdir -p "${DOWNLOAD_PATH}"

bashio::log.info "Nest Video Downloader is ready"

# Keep the container running
while true; do
    sleep 3600
done
