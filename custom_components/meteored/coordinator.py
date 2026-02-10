from datetime import timedelta
import aiohttp
import logging

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

HOURLY_URL = "https://api.meteored.com/api/forecast/v1/hourly/{hash}"
DAILY_URL = "https://api.meteored.com/api/forecast/v1/daily/{hash}"

class MeteoredDataUpdateCoordinator(DataUpdateCoordinator):

    def __init__(self, hass, entry):
        self.hass = hass
        self.entry = entry

        self.api_key = entry.data["api_key"]
        self.location_hash = entry.data["location_hash"]

        self.session = aiohttp.ClientSession()

        super().__init__(
            hass,
            _LOGGER,
            name="Meteored",
            update_interval=timedelta(hours=1),
        )

    async def _fetch(self, url):
        headers = {
            "accept": "application/json",
            "x-api-key": self.api_key,
        }

        async with self.session.get(url, headers=headers) as resp:
            if resp.status != 200:
                body = await resp.text()
                raise UpdateFailed(f"HTTP {resp.status} – {body}")
            return await resp.json()

    async def _async_update_data(self):
        hourly = await self._fetch(HOURLY_URL.format(hash=self.location_hash))
        daily = await self._fetch(DAILY_URL.format(hash=self.location_hash))

        return {
            "hourly": hourly,
            "daily": daily,
        }
