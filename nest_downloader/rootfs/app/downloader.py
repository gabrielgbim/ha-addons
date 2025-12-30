#!/usr/bin/env python3
"""
Video downloader for Nest camera events
"""

import logging
import os
import datetime
import pytz
from nest_device import NestDevice
from models import CameraEvent

logger = logging.getLogger(__name__)

# Fetch range: 4 hours (3 hours for free Nest Aware + 1 hour buffer)
DEFAULT_FETCH_RANGE = 240


class VideoDownloader:
    """Handles downloading and saving Nest camera videos"""
    
    def __init__(self, base_path: str, local_timezone: str = "America/New_York"):
        self.base_path = base_path
        self.local_timezone = local_timezone
    
    def _get_file_path(self, camera_event: CameraEvent):
        """Generate file path for camera event"""
        # Convert to local timezone for file organization
        event_local = camera_event.start_time.astimezone(pytz.timezone(self.local_timezone))
        
        # Create directory structure: base_path/device_name/year/month/day
        year = str(event_local.year)
        month = str(event_local.month).zfill(2)
        day = str(event_local.day).zfill(2)
        directory = os.path.join(
            self.base_path,
            camera_event.device_name,
            year,
            month,
            day
        )
        
        # Create filename with timestamp and duration
        timestamp_str = event_local.strftime("%Y-%m-%d_%H-%M-%S")
        
        # Add duration to filename
        total_ms = int(camera_event.duration.total_seconds() * 1000)
        secs = total_ms // 1000
        ms = total_ms % 1000
        duration_part = f"_{secs}s{ms:03d}ms"
        
        filename = f"{timestamp_str}{duration_part}.mp4"
        
        return directory, filename
    
    def _ensure_directory(self, directory):
        """Create directory if it doesn't exist"""
        os.makedirs(directory, exist_ok=True)
    
    def sync_device(self, nest_device: NestDevice, fetch_range_minutes: int = DEFAULT_FETCH_RANGE):
        """Sync videos from a single Nest device"""
        logger.info(f"Syncing {nest_device.device_name}")
        
        events = nest_device.get_events(
            end_time=datetime.datetime.now(),
            duration_minutes=fetch_range_minutes
        )
        logger.info(f"Found {len(events)} events")
        
        downloaded = 0
        skipped = 0
        
        for event in events:
            directory, filename = self._get_file_path(event)
            file_path = os.path.join(directory, filename)
            
            if os.path.exists(file_path):
                skipped += 1
                continue
            
            logger.info(f"Downloading: {filename}")
            video_data = nest_device.download_event(event)
            self._ensure_directory(directory)
            
            with open(file_path, "wb") as f:
                f.write(video_data)
            downloaded += 1
        
        logger.info(f"Downloaded: {downloaded}, Skipped: {skipped}")
