"""Platform for climate integration."""


from datetime import timedelta
import logging

import async_timeout

from homeassistant.components import bluetooth
from homeassistant.components.climate import (
    ATTR_TARGET_TEMP_HIGH,
    ATTR_TARGET_TEMP_LOW,
    FAN_AUTO,
    FAN_ON,
    PRESET_AWAY,
    PRESET_NONE,
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.const import UnitOfTemperature
from .const import DOMAIN
from bleak import BleakClient

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Ooler."""

    data = hass.data[DOMAIN]
    entities = []

    # for index in range(len(data.ecobee.thermostats)):
    #     thermostat = data.ecobee.get_thermostat(index)
    #     if thermostat["modelNumber"] not in ECOBEE_MODEL_TO_NAME:
    #         _LOGGER.error(
    #             (
    #                 "Model number for ecobee thermostat %s not recognized. "
    #                 "Please visit this link to open a new issue: "
    #                 "https://github.com/home-assistant/core/issues "
    #                 "and include the following information: "
    #                 "Unrecognized model number: %s"
    #             ),
    #             thermostat["name"],
    #             thermostat["modelNumber"],
    #         )
    #     entities.append(OolerClimate(data, index, thermostat))

    entities.append(OolerClimate(device_name=config_entry.title, address=config_entry.data["address"], data=data))
    async_add_entities(entities, True)

class OolerClimate(ClimateEntity):
    _attr_hvac_modes = [HVACMode.AUTO, HVACMode.OFF]
    _attr_temperature_unit = UnitOfTemperature.FAHRENHEIT
    _attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE
    SCAN_INTERVAL = timedelta(seconds=30)

    def __init__(self, device_name, address, data):
        self.data = {}
        self.address = address
        self.device_name = device_name

    @property
    def hvac_mode(self):
        return HVACMode.OFF

    @property
    def name(self):
        return self.device_name

    @property
    def should_poll(self):
        return True

    def ble_get_device(self, address):
        device = bluetooth.async_ble_device_from_address(self.hass, address, connectable=True)
        if not device:
            _LOGGER.error("Device with address {0} is not available".format(address))
            return
        _LOGGER.error("Got a BLE device {0}.".format(device.name))
        # client = BleakClient(device)
        # return client
        return device

    async def async_update(self):
        device = self.ble_get_device(self.address)
        if not device:
            return
        async with BleakClient(device, timeout=25.0) as client:
            _LOGGER.error("Ooler -- In client block")
            value = bytes(await client.read_gatt_char("7a2623ff-bd92-4c13-be9f-7023aa4ecb85"))
            _LOGGER.info(''.join('{:02x}'.format(x) for x in value))
            value = bytes(await client.read_gatt_char("e8ebded3-9dca-45c2-a2d8-ceffb901474d"))
            _LOGGER.info(int(''.join('{:02x}'.format(x) for x in value), 16))

    @property
    def current_temperature(self):
        return 62.3

    def set_temperature(self, **kwargs):
        """Set new target temperature."""
