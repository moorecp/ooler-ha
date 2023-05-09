from homeassistant.components import bluetooth

from .const import DOMAIN


class OolerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Ooler."""

    VERSION = 1

    async def async_step_bluetooth(self, user_input):
        """Handle bluetooth discovery."""
        return self.async_create_entry(title="Mooler", data={})
