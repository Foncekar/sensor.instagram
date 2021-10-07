import time
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import instaloader
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import STATE_UNKNOWN
from homeassistant.helpers.entity import Entity
from homeassistant.util.dt import utc_from_timestamp

ICON = "mdi:instagram"

SCAN_INTERVAL = timedelta(minutes=60)

ATTRIBUTION = "Data provided by instagram api"

DOMAIN = "instagram"

CONF_USERNAME = "username"
CONF_PASSWORD = "password"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Setup the currency sensor"""

    username = config["username"]
    password = config["password"]

    add_entities(
        [InstagramSensor(hass, username, password, SCAN_INTERVAL)],
        True,
    )

class InstagramSensor(Entity):

    def __init__(self, hass, username, password, interval):
        """Inizialize sensor"""
        self._hass = hass
        self._interval = interval
        self._username = username
        self._password = password
        self._instagram = instaloader.Instaloader()
        self._instagram.login(self._username, self._password)
        self._last_updated = STATE_UNKNOWN

    @property
    def name(self):
        """Return the name sensor"""
        return self.profile.full_name

    @property
    def icon(self):
        """Return the default icon"""
        return ICON

    @property
    def state(self):
        """Return the state of the sensor"""
        return self.profile.followers

    @property
    def last_updated(self):
        """Returns date when it was last updated."""
        if self._last_updated != 'unknown':
            stamp = float(self._last_updated)
            return utc_from_timestamp(int(stamp))

    @property
    def device_state_attributes(self):
        """Attributes."""
        return {
            "full_name": self.full_name,
            "posts": self.posts,
            "followees": self.followees,
            "followers": self.followers,
            "igtv": self.igtv,
        }

    def update(self):
        """Get the latest update fron the api"""
        self.profile = instaloader.Profile.from_username(self._instagram.context, self._username)
        self.full_name = self.profile.full_name
        self.followees = self.profile.followees
        self.followers = self.profile.followers
        self.posts = self.profile.mediacount
        self.igtv = self.profile.igtvcount
        self._last_updated = time.time()
