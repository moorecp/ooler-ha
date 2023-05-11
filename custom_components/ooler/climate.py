"""Platform for climate integration."""


from datetime import timedelta

from homeassistant.components.climate import (
    ATTR_TARGET_TEMP_HIGH,
    ATTR_TARGET_TEMP_LOW,
    FAN_LOW,
    FAN_MEDIUM,
    FAN_HIGH,
    PRESET_AWAY,
    PRESET_NONE,
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.helpers.entity import DeviceInfo
from .const import _LOGGER, DOMAIN, MANUFACTURER, MODEL

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Ooler."""

    data = hass.data[DOMAIN][config_entry.data["address"]]
    entities = []

    entities.append(OolerClimate(device_name=config_entry.title, address=config_entry.data["address"], data=data))
    async_add_entities(entities, True)

class OolerClimate(ClimateEntity):
    _attr_fan_modes = [FAN_LOW, FAN_MEDIUM, FAN_HIGH]
    _attr_hvac_modes = [HVACMode.AUTO, HVACMode.OFF]
    _attr_target_temperature_step = 1
    _attr_temperature_unit = UnitOfTemperature.FAHRENHEIT
    _attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.FAN_MODE
    SCAN_INTERVAL = timedelta(seconds=60)

    def __init__(self, device_name, address, data):
        self.data = {}
        self.address = address
        self.device_name = device_name
        self.ooler = data["ooler"]
        self.powered_on = False
        self.current_temp = 0

    @property
    def unique_id(self):
        return "{0}-climate".format(self.device_name)

    @property
    def fan_mode(self):
        if self.ooler.fan_speed == self.ooler.FanSpeed.LOW:
            return FAN_LOW
        elif self.ooler.fan_speed == self.ooler.FanSpeed.MEDIUM:
            return FAN_MEDIUM
        else:
            return FAN_HIGH

    @property
    def hvac_mode(self):
        return HVACMode.AUTO if self.ooler.is_powered_on() else HVACMode.OFF

    @property
    def name(self):
        return self.device_name

    @property
    def should_poll(self):
        return True

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={
                    (DOMAIN, self.device_name)
            },
            name=self.name,
            manufacturer=MANUFACTURER,
            model=MODEL,
        )

    async def async_update(self):
        await self.ooler.update()

    @property
    def current_temperature(self):
        return self.ooler.current_temperature

    @property
    def target_temperature(self):
        return self.ooler.temp_setpoint

    @property
    def fan_mode(self):
        return self.ooler.temp_setpoint

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        if hvac_mode == HVACMode.OFF:
            await self.ooler.power_off()
        else:
            await self.ooler.power_on()

    def set_temperature(self, **kwargs):
        """Set new target temperature."""
