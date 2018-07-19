"""
A platform which allows you to get information from Tautulli.

For more details about this component, please refer to the documentation at
https://github.com/custom-components/sensor.tautulli
"""
import requests
import voluptuous as vol
from homeassistant.helpers.entity import Entity
from homeassistant.const import (CONF_API_KEY, CONF_HOST, CONF_PORT)
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import (PLATFORM_SCHEMA)

__version__ = '0.0.1'

T_DATA = 'tautulli_data'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_PORT, default='8181'): cv.string,
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Create the sensor"""
    api_key = config.get(CONF_API_KEY)
    host = config.get(CONF_HOST)
    port = config.get(CONF_PORT)
    add_devices([Tautulli(hass, api_key, host, port)])

class Tautulli(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass, api_key, host, port):
        """Initialize the sensor."""
        self.hass = hass
        self._api_key = api_key
        self._host = host
        self._port = port 
        self._state = None
        self.hass.data[T_DATA] = {}
        self.update()

    def update(self):
        """Method to update sensor value"""
        url = 'http://' + self._host + ':' + self._port + '/api/v2?apikey=' + self._api_key + '&cmd=get_activity'
        try:
            result = requests.get(url, timeout=5).json()
        except:
            self._state = "Not playing"
        try:
            t_data = result['response']['data']['sessions'][0]
            for attribute in t_data:
                self.hass.data[T_DATA][str(attribute)] = str(t_data[attribute])
        except:
            self._state = "Not playing"
        try:
            self._state = t_data['title']
        except:
            self._state = "Not playing"

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Tautulli'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return 'mdi:plex'

    @property
    def device_state_attributes(self):
        """Return attributes for the sensor."""
        return self.hass.data[T_DATA]
