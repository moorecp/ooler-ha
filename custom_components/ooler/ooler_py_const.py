from enum import Enum

CURRENT_TEMP_UUID = "e8ebded3-9dca-45c2-a2d8-ceffb901474d"
FAN_SPEED_UUID = "cafe2421-d04c-458f-b1c0-253c6c97e8e8"
POWER_UUID = "7a2623ff-bd92-4c13-be9f-7023aa4ecb85"
SET_TEMP_UUID = "6aa46711-a29d-4f8a-88e2-044ca1fd03ff"
WATER_LEVEL_UUID = "8db5b9db-dbf6-47e6-a9dd-0612a1349a5b"

class FanSpeed(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2

class PowerStatus(Enum):
    OFF = 0
    ON = 1

class WaterLevel(Enum):
    LOW = 50
    FULL = 100
