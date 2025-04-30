"""Set up the Timezone Setter integration."""

from homeassistant.core import ServiceCall, HomeAssistant
from homeassistant.config import ConfigType
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.service import async_register_admin_service

import voluptuous as vol
from timezonefinder import TimezoneFinderL

import logging

_LOGGER = logging.getLogger(__name__)

from .const import (
    DOMAIN,
    SERVICE_SET_TIMEZONE,
    ATTR_TIMEZONE,
    ATTR_LATITUDE,
    ATTR_LONGITUDE,
)

# Instantiate once
tf = TimezoneFinderL()

# Schema that allows either timezone OR lat/lon
SERVICE_SCHEMA = vol.Schema(
    {
        vol.Optional(ATTR_TIMEZONE): cv.time_zone,
        vol.Optional(ATTR_LATITUDE): vol.Coerce(float),
        vol.Optional(ATTR_LONGITUDE): vol.Coerce(float),
    }
)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Timezone Setter integration."""

    async def async_set_timezone(call: ServiceCall) -> None:
        """Service handler to set the Home Assistant system timezone."""

        tz = call.data.get(ATTR_TIMEZONE)

        if not tz:
            # No timezone provided — try to use lat/lon
            lat = call.data.get(ATTR_LATITUDE)
            lon = call.data.get(ATTR_LONGITUDE)

            if lat is None or lon is None:
                raise ValueError("You must provide either 'timezone' or both 'latitude' and 'longitude'")

            tz = tf.timezone_at(lat=lat, lng=lon)

            # Log the raw value returned from timezonefinder
            _LOGGER.info("Resolved timezone from lat/lon: %s", tz)


            if not tz:
                raise ValueError("Could not determine timezone from latitude/longitude.")

        current_tz = hass.config.time_zone

        if tz == current_tz:
            _LOGGER.debug("Timezone unchanged (%s); skipping update.", tz)
            return

        _LOGGER.info("Changing system timezone: %s → %s", current_tz, tz)

        await hass.config.async_update(time_zone=tz)

    async_register_admin_service(
        hass,
        DOMAIN,
        SERVICE_SET_TIMEZONE,
        async_set_timezone,
        SERVICE_SCHEMA,
    )

    return True
