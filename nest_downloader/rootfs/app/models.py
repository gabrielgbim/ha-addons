#!/usr/bin/env python3
"""
Data models for Nest video events
"""

import datetime
import isodate


class CameraEvent:
    """Represents a Nest camera event with start time and duration"""
    
    def __init__(self, device_id: str, device_name: str, start_time: datetime.datetime, duration: datetime.timedelta):
        self.device_id = device_id
        self.device_name = device_name
        self.start_time = start_time
        self.duration = duration
    
    @property
    def end_time(self):
        """Calculate end time from start time and duration"""
        return self.start_time + self.duration
    
    @classmethod
    def from_xml_attrib(cls, xml_attrib: dict, device_id: str, device_name: str):
        """Create CameraEvent from XML period attributes"""
        duration = min(datetime.timedelta(minutes=1), isodate.parse_duration(xml_attrib["duration"]))
        
        return cls(
            device_id=device_id,
            device_name=device_name,
            start_time=datetime.datetime.fromisoformat(xml_attrib["programDateTime"]),
            duration=duration
        )
    
    def __str__(self):
        return f"CameraEvent({self.device_name}, {self.start_time}, {self.duration})"
