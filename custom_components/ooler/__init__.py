"""Support for Ooler."""
# from datetime import timedelta

# from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
# from homeassistant.const import CONF_API_KEY, CONF_NAME, Platform
# from homeassistant.core import HomeAssistant
# from homeassistant.helpers import config_validation as cv, discovery
# from homeassistant.helpers.typing import ConfigType
# from homeassistant.util import Throttle

from ooler_py.Ooler import Ooler
from .const import (
    _LOGGER,
    DOMAIN,
    PLATFORMS,
)

# MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=60)


async def async_setup(hass, config):
#     """Ecobee uses config flow for configuration.

#     But, an "ecobee:" entry in configuration.yaml will trigger an import flow
#     if a config entry doesn't already exist. If ecobee.conf exists, the import
#     flow will attempt to import it and create a config entry, to assist users
#     migrating from the old ecobee integration. Otherwise, the user will have to
#     continue setting up the integration via the config flow.
#     """

    hass.data[DOMAIN] = config.get(DOMAIN, {})
#     hass.data[DATA_HASS_CONFIG] = config

#     if not hass.config_entries.async_entries(DOMAIN) and hass.data[DATA_ECOBEE_CONFIG]:
#         # No config entry exists and configuration.yaml config exists, trigger the import flow.
#         hass.async_create_task(
#             hass.config_entries.flow.async_init(
#                 DOMAIN, context={"source": SOURCE_IMPORT}
#             )
#         )

    return True


async def async_setup_entry(hass, entry):
    """Set up an Ooler."""
    if hass.data[DOMAIN] is None:
        hass.data[DOMAIN] = {}
    _LOGGER.error("__init__ AES: {0}".format(entry.as_dict()))
    hass.data[DOMAIN][entry.data["address"]] = {"address": entry.data["address"], "name": entry.title, "ooler": Ooler(address)}
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


# class OolerData:
#     """Handle getting the latest data from ecobee.com so platforms can use it.

#     Also handle refreshing tokens and updating config entry with refreshed tokens.
#     """

#     def __init__(
#         self, hass: HomeAssistant, entry: ConfigEntry, api_key: str, refresh_token: str
#     ) -> None:
#         """Initialize the Ecobee data object."""
#         self._hass = hass
#         self._entry = entry
#         self.ecobee = Ecobee(
#             config={ECOBEE_API_KEY: api_key, ECOBEE_REFRESH_TOKEN: refresh_token}
#         )

#     @Throttle(MIN_TIME_BETWEEN_UPDATES)
#     async def update(self):
#         """Get the latest data from the Ooler unit."""
#         await self._hass.async_add_executor_job(self.ooler.update)
#         _LOGGER.debug("Updating Ooler")


async def async_unload_entry(hass, entry):
    """Unload the config entry and platforms."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data.pop(DOMAIN)
    return unload_ok
