import asyncio
from bleak import BleakClient, BleakScanner
from collections import deque
from threading import Thread
from .const import (
    CURRENT_TEMP_UUID,
    FAN_SPEED_UUID,
    POWER_UUID,
    SET_TEMP_UUID,
    WATER_LEVEL_UUID,
    FanSpeed,
    PowerStatus,
    WaterLevel,
)

class Ooler:
    def __init__(self, address):
        self.address = address
        self.message_queue = deque([])
        self.current_temperature = 55
        self.fan_speed = FanSpeed.LOW
        self.power_status = PowerStatus.OFF
        self.temp_setpoint = 55
        self.water_level = WaterLevel.FULL

        self.update()

    async def enqueue_message(self, characteristic, value=None, callback=None):
        call_function = len(self.message_queue) == 0
        self.message_queue.append({"callback": callback, "characteristic": characteristic, "value": value})
        if call_function:
            thread = Thread(target=self.enqueue_process_queue)
            thread.start()

    def enqueue_process_queue(self):
        task = asyncio.run(self.process_queue())

    async def process_queue(self):
        print("Messages: {0}".format(len(self.message_queue)))
        try:
            message = self.message_queue.popleft()
            device = await BleakScanner.find_device_by_address(self.address, timeout=25.0)
            async with BleakClient(device, timeout=50.0) as client:
                while True:
                    response = None
                    if message["value"] is None:
                        response = await client.read_gatt_char(message["characteristic"])
                        if message["callback"] is not None:
                            await message["callback"](response)
                    else:
                        await client.write_gatt_char(message["characteristic"], bytes.fromhex(message["value"]))
                    message = self.message_queue.popleft()
        except IndexError:
            return

    def update(self):
        background_tasks = set()
        task = asyncio.create_task(self.get_current_temperature())
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)

        task = asyncio.create_task(self.get_fan_speed())
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)

        task = asyncio.create_task(self.get_power_status())
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)

        task = asyncio.create_task(self.get_temp_setpoint())
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)

        task = asyncio.create_task(self.get_water_level())
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)

    async def get_current_temperature(self):
        await self.enqueue_message(CURRENT_TEMP_UUID, callback=self.assign_current_temperature)
    async def assign_current_temperature(self, value):
        self.current_temperature = int.from_bytes(value, byteorder="big")

    async def get_fan_speed(self):
        await self.enqueue_message(FAN_SPEED_UUID, callback=self.assign_fan_speed)
    async def assign_fan_speed(self, value):
        self.fan_speed = int.from_bytes(value, byteorder="big")

    async def get_power_status(self):
        await self.enqueue_message(POWER_UUID, callback=self.assign_power_status)
    async def assign_power_status(self, value):
        self.power_status = int.from_bytes(value, byteorder="big")

    async def get_temp_setpoint(self):
        await self.enqueue_message(SET_TEMP_UUID, callback=self.assign_temp_setpoint)
    async def assign_temp_setpoint(self, value):
        self.temp_setpoint = int.from_bytes(value, byteorder="big")

    async def get_water_level(self):
        await self.enqueue_message(WATER_LEVEL_UUID, callback=self.assign_water_level)
    async def assign_water_level(self, value):
        self.water_level = int.from_bytes(value, byteorder="big")

    async def power_on(self):
        await self.enqueue_message(POWER_UUID, callback=self.powered_on, value=PowerStatus.ON)
    async def powered_on(self):
        self.assign_power_status(PowerStatus.ON)
    async def power_off(self):
        await self.enqueue_message(POWER_UUID, callback=self.powered_off, value=PowerStatus.OFF)
    async def powered_off(self):
        self.assign_power_status(PowerStatus.OFF)
    def is_powered_on(self):
        return self.power_status == PowerStatus.ON
