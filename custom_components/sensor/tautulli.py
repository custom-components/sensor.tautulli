"""
A platform which allows you to get information from Tautulli.

For more details about this component, please refer to the documentation at
https://github.com/custom-components/sensor.tautulli
"""

import logging
import voluptuous as vol
from homeassistant.helpers.entity import Entity
from homeassistant.const import (CONF_API_KEY, CONF_HOST, CONF_PORT)
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import (PLATFORM_SCHEMA)

__version__ = '0.1.0'

REQUIREMENTS = ['pytautulli==0.0.5']

_LOGGER = logging.getLogger(__name__)

CONF_ATTRIBUTES = 'attributes'
CONF_USERS = 'users'
T_DATA = 'tautulli_data'
TU_DATA = 'tautulli_user_data_'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_PORT, default='8181'): cv.string,
    vol.Optional(CONF_ATTRIBUTES, default='None'):
        vol.All(cv.ensure_list, [cv.string]),
    vol.Optional(CONF_USERS, default='None'):
        vol.All(cv.ensure_list, [cv.string]),
    })

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Create the sensor"""
    import pytautulli
    api_key = config.get(CONF_API_KEY)
    host = config.get(CONF_HOST)
    port = config.get(CONF_PORT)
    keys = config.get(CONF_ATTRIBUTES)
    users = config.get(CONF_USERS)
    tautulli = pytautulli
    usernames = tautulli.get_users(host, port, api_key)
    for user in usernames:
        _LOGGER.debug(user)
        if user in users or 'None' in users:
            add_devices([TautulliUser(hass, tautulli, api_key, host, port, user, keys)])
    add_devices([Tautulli(hass, tautulli, api_key, host, port)])

class Tautulli(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass, tautulli, api_key, host, port):
        """Initialize the sensor."""
        self.hass = hass
        self.tautulli = tautulli
        self._api_key = api_key
        self._host = host
        self._port = port
        self._state = None
        self.hass.data[T_DATA] = {}
        self.update()

    def update(self):
        """Method to update sensor value"""
        from time import gmtime, strftime
        self._state = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        stats = self.tautulli.get_home_stats(self._host,
                                             self._port, self._api_key)
        for key in stats:
            self.hass.data[T_DATA][str(key)] = str(stats[key])

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

class TautulliUser(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass, tautulli, api_key, host, port, username, keys):
        """Initialize the sensor."""
        self.hass = hass
        self.tautulli = tautulli
        self._api_key = api_key
        self._keys = keys
        self._host = host
        self._port = port
        self._username = username
        self._state = None
        self.hass.data[TU_DATA + str(self._username)] = {}
        self.update()

    def update(self):
        """Method to update sensor value"""
        self._state = self.tautulli.get_user_state(self._host,
                                                   self._port, self._api_key, self._username)
        attrlist = self.tautulli.get_user_activity(self._host,
                                                   self._port, self._api_key, self._username)
        for key in self._keys:
            try:
                self.hass.data[TU_DATA + str(self._username)][str(key)] = str(attrlist[key])
            except:
                self.hass.data[TU_DATA + str(self._username)][str(key)] = ''

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Tautulli - ' + self._username

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
        return self.hass.data[TU_DATA + str(self._username)]
