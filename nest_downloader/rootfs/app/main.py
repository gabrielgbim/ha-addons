#!/usr/bin/env python3
"""
Nest Video Downloader - Home Assistant Add-on
Main application entry point
"""

import os
import sys
import logging
import time

# Print to stdout immediately before any other setup
print("=== MAIN.PY STARTING ===", flush=True)

try:
    print("Importing auth...", flush=True)
    from auth import GoogleAuthenticator
    print("Importing nest_device...", flush=True)
    from nest_device import NestDevice
    print("Importing downloader...", flush=True)
    from downloader import VideoDownloader
    print("All imports successful!", flush=True)
except Exception as e:
    print(f"IMPORT ERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Use Home Assistant's logging configuration
logger = logging.getLogger(__name__)
print("Logger configured, testing logger...", flush=True)
logger.info("Logger initialized")
print("After logger test", flush=True)


class Config:
    """Configuration loaded from Home Assistant add-on options"""
    
    def __init__(self):
        self.base_path = os.getenv('BASE_PATH')
        self.google_username = os.getenv('GOOGLE_USERNAME')
        self.google_master_token = os.getenv('GOOGLE_MASTER_TOKEN')
        self.local_timezone = os.getenv('LOCAL_TIMEZONE', 'America/New_York')
        self.refresh_interval = int(os.getenv('REFRESH_INTERVAL', 60))
        
        # Validate required configuration
        if not self.base_path:
            raise ValueError("BASE_PATH is required")
        if not self.google_username:
            raise ValueError("GOOGLE_USERNAME is required")
        if not self.google_master_token:
            raise ValueError("GOOGLE_MASTER_TOKEN is required")
    
    def display(self):
        """Display configuration (without sensitive data)"""
        logger.info(f"Base Path: {self.base_path}")
        logger.info(f"Google Username: {self.google_username}")
        logger.info(f"Google Master Token: {'*' * len(self.google_master_token) if self.google_master_token else '(not set)'}")
        logger.info(f"Local Timezone: {self.local_timezone}")
        logger.info(f"Refresh Interval: {self.refresh_interval} minutes")


class NestDownloader:
    """Main application class for Nest Video Downloader"""
    
    def __init__(self, config):
        self.config = config
        logger.info("Initializing Nest Video Downloader...")
        
        # Initialize authenticator
        self.authenticator = GoogleAuthenticator(
            username=config.google_username,
            master_token=config.google_master_token
        )
        
        # Get Nest devices
        logger.info("Discovering Nest devices...")
        device_list = self.authenticator.get_nest_devices()
        
        if not device_list:
            logger.warning("No Nest devices found!")
            self.devices = []
        else:
            self.devices = [
                NestDevice(dev['id'], dev['name'], self.authenticator)
                for dev in device_list
            ]
            logger.info(f"Found {len(self.devices)} Nest device(s)")
        
        # Initialize video downloader
        self.downloader = VideoDownloader(
            base_path=config.base_path,
            local_timezone=config.local_timezone
        )
        
        logger.info("Nest Video Downloader initialized")
    
    def sync_all_devices(self):
        """Sync videos from all devices"""
        if not self.devices:
            logger.warning("No devices to sync")
            return
        
        logger.info("Starting sync for all devices...")
        for device in self.devices:
            try:
                self.downloader.sync_device(device)
            except Exception as e:
                logger.error(f"Error syncing device {device.device_name}: {e}", exc_info=True)
        logger.info("Sync completed")
    
    def run(self):
        """Main application loop"""
        logger.info("Starting main application loop...")
        
        while True:
            try:
                self.sync_all_devices()
                
                # Sleep for the configured interval
                sleep_seconds = self.config.refresh_interval * 60
                logger.info(f"Waiting {self.config.refresh_interval} minutes until next check...")
                time.sleep(sleep_seconds)
                
            except KeyboardInterrupt:
                logger.info("Received interrupt signal, shutting down...")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}", exc_info=True)
                logger.info("Waiting 60 seconds before retrying...")
                time.sleep(60)


def main():
    """Main entry point"""
    logger.info("=== Nest Video Downloader Starting ===")
    
    try:
        # Load configuration
        config = Config()
        
        logger.info("Configuration loaded:")
        config.display()
        
        # Create and run application
        app = NestDownloader(config)
        app.run()
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    print("Calling main()...", flush=True)
    main()
    print("main() completed", flush=True)
