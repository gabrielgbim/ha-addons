#!/usr/bin/env python3
"""
Google Authentication for Nest API
"""

import logging
import datetime
import glocaltokens.client

logger = logging.getLogger(__name__)


class GLocalAuthenticationTokensMultiService(glocaltokens.client.GLocalAuthenticationTokens):
    """Extended GLocalAuthenticationTokens to support multiple services"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_access_token_service = None
    
    def get_access_token(self, service=glocaltokens.client.ACCESS_TOKEN_SERVICE):
        """Return existing or fetch access_token for specified service"""
        if (
            self.access_token is None
            or self.access_token_date is None
            or self._has_expired(self.access_token_date, glocaltokens.client.ACCESS_TOKEN_DURATION)
            or self._last_access_token_service != service
        ):
            logger.debug("Getting new access token...")
            master_token = self.get_master_token()
            if master_token is None:
                logger.error("Unable to obtain master token")
                return None
            if self.username is None:
                logger.error("Username is not set")
                return None
            
            res = glocaltokens.client.perform_oauth(
                self._escape_username(self.username),
                master_token,
                self.get_android_id(),
                app=glocaltokens.client.ACCESS_TOKEN_APP_NAME,
                service=service,
                client_sig=glocaltokens.client.ACCESS_TOKEN_CLIENT_SIGNATURE,
            )
            
            if "Auth" not in res:
                logger.error("Could not get access token")
                logger.debug(f"Request response: {res}")
                return None
            
            self.access_token = res["Auth"]
            self.access_token_date = datetime.datetime.now()
            self._last_access_token_service = service
        
        return self.access_token


class GoogleAuthenticator:
    """Handles Google authentication for Nest services"""
    
    NEST_SCOPE = "oauth2:https://www.googleapis.com/auth/nest-account"
    
    def __init__(self, username, master_token):
        self._auth = GLocalAuthenticationTokensMultiService(
            username=username,
            master_token=master_token,
            password="FAKE_PASSWORD"
        )
        logger.info(f"Initialized Google authenticator for {username}")
    
    def get_nest_access_token(self):
        """Get access token for Nest API"""
        access_token = self._auth.get_access_token(service=self.NEST_SCOPE)
        if not access_token:
            raise Exception("Couldn't get a Nest access token")
        return access_token
    
    def get_nest_devices(self):
        """Get list of Nest camera devices from homegraph"""
        try:
            homegraph_response = self._auth.get_homegraph()
            devices = []
            
            for device in homegraph_response.home.devices:
                # Look for devices with camera streaming and Nest model
                if ("action.devices.traits.CameraStream" in device.traits and 
                    "Nest" in device.hardware.model):
                    device_info = {
                        'id': device.device_info.agent_info.unique_id,
                        'name': device.device_name
                    }
                    devices.append(device_info)
                    logger.info(f"Found Nest device: {device_info['name']} ({device_info['id']})")
            
            return devices
        except Exception as e:
            logger.error(f"Error getting Nest devices: {e}")
            raise
