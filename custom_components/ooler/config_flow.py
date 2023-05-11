from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigFlow
from homeassistant.helpers import config_entry_flow

from .const import _LOGGER, DOMAIN
from .Ooler import Ooler

class OolerConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Ooler."""

    VERSION = 1

    async def async_step_bluetooth(self, discovery_info):
        """Handle bluetooth discovery."""
        _LOGGER.error("Discovered {0} at {1}".format(discovery_info.name, discovery_info.address))
        for entry in self.hass.config_entries.async_entries(DOMAIN):
            if entry.data["address"] == discovery_info.address:
                _LOGGER.error("Skipping device: {0}. Already added.".format(discovery_info.name))
                return
        _LOGGER.error("Adding entry: {0}".format(discovery_info.name))
        data = self.hass.data[DOMAIN][discovery_info.address]
        data["ooler"] = Ooler(self.hass, discovery_info.address)
        self.hass.data[DOMAIN][discovery_info.address] = data

        return self.async_create_entry(title=discovery_info.name, data={"address": discovery_info.address})

    # config_entry_flow.register_discovery_flow(DOMAIN, "Ooler", _async_has_devices)
