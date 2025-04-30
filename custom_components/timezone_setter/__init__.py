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

def validate_timezone_or_coordinates(data):
    has_timezone = "timezone" in data
    has_lat = "latitude" in data
    has_lon = "longitude" in data

    if has_timezone and (has_lat or has_lon):
        raise vol.Invalid("Provide either 'timezone' or a 'latitude' AND 'longitude', not all three.")

    if (has_lat and not has_lon) or (has_lon and not has_lat):
        raise vol.Invalid("Both 'latitude' and 'longitude' must be provided together.")

    if not has_timezone and not (has_lat and has_lon):
        raise vol.Invalid("You must provide either 'timezone' or a 'latitude' and 'longitude'.")

    return data

# Schema that allows either timezone OR lat/lon
SERVICE_SCHEMA = vol.All(
    vol.Schema({
        vol.Optional("timezone"): cv.string,
        vol.Optional("latitude"): vol.All(vol.Coerce(float), vol.Range(min=-90, max=90)),
        vol.Optional("longitude"): vol.All(vol.Coerce(float), vol.Range(min=-180, max=180)),
    }),
    validate_timezone_or_coordinates
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
