"""Platform for climate integration."""


from datetime import timedelta
import logging

import async_timeout

from homeassistant.components.climate import ClimateEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# async def async_setup_entry(
#     hass: HomeAssistant,
#     config_entry: ConfigEntry,
#     async_add_entities: AddEntitiesCallback,
# ) -> None:
#     """Set up the ecobee thermostat."""

#     data = hass.data[DOMAIN]
#     entities = []

#     for index in range(len(data.ecobee.thermostats)):
#         thermostat = data.ecobee.get_thermostat(index)
#         if thermostat["modelNumber"] not in ECOBEE_MODEL_TO_NAME:
#             _LOGGER.error(
#                 (
#                     "Model number for ecobee thermostat %s not recognized. "
#                     "Please visit this link to open a new issue: "
#                     "https://github.com/home-assistant/core/issues "
#                     "and include the following information: "
#                     "Unrecognized model number: %s"
#                 ),
#                 thermostat["name"],
#                 thermostat["modelNumber"],
#             )
#         entities.append(OolerClimate(data, index, thermostat))

#     async_add_entities(entities, True)

class OolerClimate(ClimateEntity):
    _attr_temperature_unit = TEMP_FAHRENHEIT
    SCAN_INTERVAL = timedelta(seconds=30)

    def __init__(self):
        self.should_poll = True
        self.data = {}

    def ble_get_client(address):
        device = bluetooth.async_ble_device_from_address(hass, address)
        if not device:
            log.error("Device with address {0} is not available".format(address))
            return

        client = BleakClient(device)
        return client

    async def async_update():
        client = self.ble_get_client("60:A4:23:F1:F2:72")
        value = bytes(await client.read_gatt_char("7a2623ff-bd92-4c13-be9f-7023aa4ecb85"))
        log.info(''.join('{:02x}'.format(x) for x in value))

    def set_temperature(self, **kwargs):
        """Set new target temperature."""
