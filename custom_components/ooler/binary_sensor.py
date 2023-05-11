"""Platform for binary sensor integration."""


from datetime import timedelta

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.helpers.entity import DeviceInfo
from .const import _LOGGER, DOMAIN, MANUFACTURER, MODEL

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Ooler."""

    data = hass.data[DOMAIN][config_entry.data["address"]]
    entities = []

    entities.append(OolerLowWaterBinarySensor(device_name=config_entry.title, address=config_entry.data["address"], data=data))
    async_add_entities(entities, True)

class OolerLowWaterBinarySensor(BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.MOISTURE
    SCAN_INTERVAL = timedelta(seconds=60)

    def __init__(self, device_name, address, data):
        self.ooler = data["ooler"]
        self.address = address
        self.device_name = device_name
        self.water_level = 100

    @property
    def unique_id(self):
        return "{0}-low-water".format(self.device_name)

    @property
    def name(self):
        return "Low Water"

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

    @property
    def is_on(self):
        return self.ooler.water_level != 100

    async def async_update(self):
        await self.ooler.get_water_level()
