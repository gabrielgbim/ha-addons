#!/usr/bin/env python3
"""
Nest Camera Device API
"""

import logging
import datetime
import pytz
import requests
import xml.etree.ElementTree as ET
from models import CameraEvent

logger = logging.getLogger(__name__)


class NestDevice:
    """Represents a Nest camera device and handles API interactions"""
    
    NEST_API_DOMAIN = "https://nest-camera-frontend.googleapis.com"
    EVENTS_URI = NEST_API_DOMAIN + "/dashmanifest/namespace/nest-phoenix-prod/device/{device_id}"
    DOWNLOAD_VIDEO_URI = NEST_API_DOMAIN + "/mp4clip/namespace/nest-phoenix-prod/device/{device_id}"
    
    def __init__(self, device_id, device_name, authenticator):
        self.device_id = device_id
        self.device_name = device_name
        self._authenticator = authenticator
    
    def _make_request(self, url, params=None):
        """Make authenticated GET request to Nest API"""
        url = url.format(device_id=self.device_id)
        access_token = self._authenticator.get_nest_access_token()
        response = requests.get(
            url=url,
            params=params or {},
            headers={"Authorization": f"Bearer {access_token}"}
        )
        response.raise_for_status()
        return response.content
    
    def _parse_events_xml(self, events_xml):
        """Parse events from XML response"""
        root = ET.fromstring(events_xml)
        periods = root.findall(".//{urn:mpeg:dash:schema:mpd:2011}Period")
        return [CameraEvent.from_xml_attrib(period.attrib, self.device_id, self.device_name) 
                for period in periods]
    
    def get_events(self, end_time: datetime.datetime, duration_minutes: int):
        """Get camera events within a time range"""
        start_time = end_time - datetime.timedelta(minutes=duration_minutes)
        start_utc = start_time.astimezone(pytz.timezone("UTC")).isoformat()[:-9] + "Z"
        end_utc = end_time.astimezone(pytz.timezone("UTC")).isoformat()[:-9] + "Z"
        
        params = {
            "start_time": start_utc,
            "end_time": end_utc,
            "types": 4,
            "variant": 2,
        }
        
        response = self._make_request(self.EVENTS_URI, params=params)
        return self._parse_events_xml(response)
    
    def download_event(self, camera_event: CameraEvent):
        """Download video for a specific camera event"""
        params = {
            "start_time": int(camera_event.start_time.timestamp() * 1000),
            "end_time": int(camera_event.end_time.timestamp() * 1000),
        }
        return self._make_request(self.DOWNLOAD_VIDEO_URI, params=params)
