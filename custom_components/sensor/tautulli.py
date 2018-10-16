"""
A platform which allows you to get information from Tautulli.

For more details about this component, please refer to the documentation at
https://github.com/custom-components/sensor.tautulli
"""

import logging
import voluptuous as vol
from homeassistant.helpers.entity import Entity
from homeassistant.const import (CONF_API_KEY, CONF_HOST, CONF_PORT, CONF_SSL)
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import (PLATFORM_SCHEMA)

__version__ = '0.2.2'

REQUIREMENTS = ['pytautulli==0.1.3']

_LOGGER = logging.getLogger(__name__)

CONF_ATTRIBUTES = 'attributes'
CONF_USERS = 'users'
T_DATA = 'tautulli_data'
TU_DATA = 'tautulli_user_data_'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_PORT, default='8181'): cv.string,
    vol.Optional(CONF_SSL, default=False): cv.boolean,
    vol.Optional(CONF_ATTRIBUTES, default='None'):
        vol.All(cv.ensure_list, [cv.string]),
    vol.Optional(CONF_USERS, default='None'):
        vol.All(cv.ensure_list, [cv.string]),
    })


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Create the sensor."""
    import pytautulli
    schema = 'http'
    api_key = config.get(CONF_API_KEY)
    host = config.get(CONF_HOST)
    port = config.get(CONF_PORT)
    keys = config.get(CONF_ATTRIBUTES)
    users = config.get(CONF_USERS)
    ssl = config.get(CONF_SSL)
    if ssl:
        schema = 'https'
    usernames = pytautulli.get_users(host, port, api_key, schema)
    for user in usernames:
        _LOGGER.debug(user)
        if user in users or 'None' in users:
            add_devices([TautulliUser(api_key, host, port,
                                      user, keys, schema)])
    add_devices([Tautulli(api_key, host, port, schema)])


class Tautulli(Entity):
    """Representation of a Sensor."""

    def __init__(self, api_key, host, port, schema):
        """Initialize the sensor."""
        import pytautulli
        self.tautulli = pytautulli
        self.data = {}
        self._api_key = api_key
        self._host = host
        self._port = port
        self._schema = schema
        self._state = None
        self.update()

    def update(self):
        """Update sensor value."""
        most_stats = self.tautulli.get_most_stats(self._host,
                                                  self._port,
                                                  self._api_key,
                                                  self._schema)
        for key in most_stats:
            self.data[str(key)] = str(most_stats[key])

        sever_stats = self.tautulli.get_server_stats(self._host,
                                                     self._port,
                                                     self._api_key,
                                                     self._schema)
        for key in sever_stats:
            self.data[str(key)] = str(sever_stats[key])

        self._state = sever_stats['count']

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
        return self.data


class TautulliUser(Entity):
    """Representation of a Sensor."""

    def __init__(self, api_key, host, port, username, keys, schema):
        """Initialize the sensor."""
        import pytautulli
        self.tautulli = pytautulli
        self.data = {}
        self._api_key = api_key
        self._keys = keys
        self._host = host
        self._port = port
        self._schema = schema
        self._username = username
        self.data[str(self._username)] = {}
        self._state = None
        self.update()

    def update(self):
        """Update sensor value."""
        self._state = self.tautulli.get_user_state(self._host,
                                                   self._port,
                                                   self._api_key,
                                                   self._username,
                                                   self._schema)
        attrlist = self.tautulli.get_user_activity(self._host,
                                                   self._port,
                                                   self._api_key,
                                                   self._username,
                                                   self._schema)
        for key in self._keys:
            try:
                self.data[str(self._username)][str(key)] = str(attrlist[key])
            except KeyError:
                self.data[str(self._username)][str(key)] = ''

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
        return self.data[str(self._username)]
