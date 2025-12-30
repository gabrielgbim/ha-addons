#!/usr/bin/env python3
"""
Data models for Nest video events
"""

import logging
import datetime
from typing import Optional
from pydantic import BaseModel
import isodate

logger = logging.getLogger(__name__)


class CameraEvent(BaseModel):
    """Represents a Nest camera event with start time and duration"""
    
    device_id: str
    device_name: str
    start_time: datetime.datetime
    duration: datetime.timedelta
    event_type: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True
    
    @property
    def end_time(self):
        """Calculate end time from start time and duration"""
        return self.start_time + self.duration
    
    @property
    def event_id(self):
        """Unique identifier for this event"""
        return f"{self.start_time.isoformat()}->{self.end_time.isoformat()}|{self.device_id}"
    
    @classmethod
    def from_xml_attrib(cls, xml_attrib: dict, device_id: str, device_name: str):
        """Create CameraEvent from XML period attributes"""
        # Extract event type if available
        event_type = None
        for key in ("eventType", "type", "event", "category", "event-type"):
            if key in xml_attrib:
                event_type = xml_attrib.get(key)
                break
        
        # Parse duration and cap at 1 minute
        duration = isodate.parse_duration(xml_attrib["duration"])
        duration = min(datetime.timedelta(minutes=1), duration)
        
        return cls(
            device_id=device_id,
            device_name=device_name,
            start_time=datetime.datetime.fromisoformat(xml_attrib["programDateTime"]),
            duration=duration,
            event_type=event_type
        )
    
    def __str__(self):
        return f"CameraEvent({self.device_name}, {self.start_time}, {self.duration})"
