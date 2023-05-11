import logging
from homeassistant.const import Platform

_LOGGER = logging.getLogger(__package__)

DOMAIN = "ooler"
MANUFACTURER = "Sleepme Inc."
MODEL = "Ooler"
PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.CLIMATE,
]
