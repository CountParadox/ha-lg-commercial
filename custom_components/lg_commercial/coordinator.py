import asyncio
import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

class LGDisplayAPI:
    def __init__(self, host, port, mac, use_alternate=False, set_id="01"):
        self.host = host
        self.port = port
        self.mac = mac
        self.use_alternate = use_alternate
        self.set_id = set_id

    async def send(self, command):
        reader, writer = await asyncio.open_connection(self.host, self.port)
        writer.write(f"{command}\r".encode())
        await writer.drain()
        data = await reader.read(128)
        writer.close()
        await writer.wait_closed()
        return data.decode(errors="ignore")

    async def power_on(self):
        return await self.send(f"ka {self.set_id} 01")

    async def power_off(self):
        return await self.send(f"ka {self.set_id} 00")

    async def get_power(self):
        return await self.send(f"ka {self.set_id} ff")

    async def set_input(self, code):
        cmd = "xv" if self.use_alternate else "xb"
        return await self.send(f"{cmd} {self.set_id} {code}")

    async def get_input(self):
        cmd = "xv" if self.use_alternate else "xb"
        return await self.send(f"{cmd} {self.set_id} ff")

    async def set_volume(self, value):
        return await self.send(f"kf {self.set_id} {value:02}")

    async def get_volume(self):
        return await self.send(f"kf {self.set_id} ff")

    async def set_mute(self, mute):
        val = "01" if mute else "00"
        return await self.send(f"ke {self.set_id} {val}")

    async def get_mute(self):
        return await self.send(f"ke {self.set_id} ff")

    async def set_lcn(self, lcn):
        return await self.send(f"ma {self.set_id} {lcn:03}")

class LGCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api):
        super().__init__(
            hass,
            _LOGGER,
            name="LG Commercial",
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.api = api

    async def _async_update_data(self):
        try:
            power = await self.api.get_power()
            input_state = await self.api.get_input()
            volume = await self.api.get_volume()
            mute = await self.api.get_mute()

            return {
                "power": power,
                "input": input_state,
                "volume": volume,
                "mute": mute,
            }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with LG display: {err}")
