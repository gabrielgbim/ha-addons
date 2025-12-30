#!/usr/bin/env python3
"""
Nest Video Downloader - Home Assistant Add-on
Main application entry point
"""

import os
import sys
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)


class Config:
    """Configuration loaded from Home Assistant add-on options"""
    
    def __init__(self):
        self.base_path = os.getenv('BASE_PATH')
        self.google_username = os.getenv('GOOGLE_USERNAME')
        self.google_master_token = os.getenv('GOOGLE_MASTER_TOKEN')
        self.local_timezone = os.getenv('LOCAL_TIMEZONE')
        self.refresh_interval = int(os.getenv('REFRESH_INTERVAL'))
    
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
        logger.info("Nest Video Downloader initialized")
    
    def run(self):
        """Main application loop"""
        logger.info("Starting main application loop...")
        
        while True:
            try:
                logger.info("Checking for new videos...")
                # TODO: Implement Nest API integration
                # - Authenticate with Google/Nest
                # - Get list of cameras
                # - Download new videos to base_path
                
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
        # Load and validate configuration
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
    main()
