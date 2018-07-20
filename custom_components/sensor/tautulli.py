"""
A platform which allows you to get information from Tautulli.

For more details about this component, please refer to the documentation at
https://github.com/custom-components/sensor.tautulli
"""
import requests
import logging
import voluptuous as vol
from homeassistant.helpers.entity import Entity
from homeassistant.const import (CONF_API_KEY, CONF_HOST, CONF_PORT,CONF_USERNAME)
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import (PLATFORM_SCHEMA)

__version__ = '0.0.2'

_LOGGER = logging.getLogger(__name__)

CONF_KEYS = 'keys'
T_DATA = 'tautulli_data'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Optional(CONF_PORT, default='8181'): cv.string,
    vol.Required(CONF_KEYS, default='None'):
        vol.All(cv.ensure_list, [cv.string]),
    })

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Create the sensor"""
    api_key = config.get(CONF_API_KEY)
    host = config.get(CONF_HOST)
    port = config.get(CONF_PORT)
    keys = config.get(CONF_KEYS)
    username = config.get(CONF_USERNAME)
    add_devices([Tautulli(hass, api_key, host, port, keys, username)])

class Tautulli(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass, api_key, host, port, keys, username):
        """Initialize the sensor."""
        self.hass = hass
        self._api_key = api_key
        self._host = host
        self._port = port 
        self._keys = keys
        self._username = username
        self._state = None
        self.hass.data[T_DATA] = {}
        self.update()

    def update(self):
        """Method to update sensor value"""
        url = "http://{}:{}/api/v2?apikey={}&cmd=get_activity".format(self._host, self._port, self._api_key)
        num = 0
        try:
            result = requests.get(url, timeout=5).json()
        except:
            self._state = "Not playing"
        try:
            t_data = result['response']['data']['sessions']
            for sessions in t_data:
                if t_data[num]['username'].lower() == self._username.lower():
                    t_data = t_data[num]
                    for key in self._keys:
                        try:
                            self.hass.data[T_DATA][str(key)] = str(t_data[key])
                        except:
                            _LOGGER.debug('%s not found.', key)
                else:
                    num = num + 1
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
