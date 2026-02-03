from __future__ import annotations

import async_timeout
from datetime import datetime, timezone

from homeassistant.components.weather import WeatherEntity, Forecast
from homeassistant.const import (
    TEMP_CELSIUS,
    PRESSURE_HPA,
    SPEED_KILOMETERS_PER_HOUR,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, BASE_URL, ATTRIBUTION


def ms_to_datetime(ms: int):
    if not ms:
        return None
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)


def symbol_to_condition(symbol: int) -> str:
    if symbol == 1:
        return "sunny"
    if symbol in (2, 3, 4):
        return "partlycloudy"
    if symbol == 5:
        return "cloudy"
    if symbol in (6, 7):
        return "windy-variant"
    if symbol in (8, 9):
        return "fog"
    if symbol in (12, 13, 14, 15, 16, 17):
        return "rainy"
    if symbol in (18, 19, 20, 21, 22, 23):
        return "snowy-rainy"
    if symbol in (24, 25, 26, 27):
        return "snowy"
    if symbol in (28, 29):
        return "pouring"
    if symbol in (30, 31):
        return "snowy-rainy"
    if symbol in (32, 33):
        return "snowy"
    if symbol in (10, 11):
        return "lightning"
    if symbol in (34, 35, 38, 39):
        return "lightning-rainy"
    if symbol in (36, 37):
        return "hail"
    if symbol in (40, 41):
        return "exceptional"
    return "cloudy"


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([MeteoredWeather(hass, entry)], True)


class MeteoredWeather(WeatherEntity):
    _attr_temperature_unit = TEMP_CELSIUS
    _attr_pressure_unit = PRESSURE_HPA
    _attr_wind_speed_unit = SPEED_KILOMETERS_PER_HOUR
    _attr_attribution = ATTRIBUTION

    def __init__(self, hass, entry):
        self.hass = hass
        self._api_key = entry.data["api_key"]
        self._hash = entry.data["hash"]
        self._attr_name = "Meteored"
        self._data = None

    async def async_update(self):
        session = async_get_clientsession(self.hass)
        url = f"{BASE_URL}/{self._hash}"
        headers = {"x-api-key": self._api_key}

        async with async_timeout.timeout(10):
            resp = await session.get(url, headers=headers)
            self._data = await resp.json()

    @property
    def temperature(self):
        return self._data["data"]["days"][0]["temperature_max"]

    @property
    def condition(self):
        return symbol_to_condition(self._data["data"]["days"][0]["symbol"])

    @property
    def forecast(self):
        forecasts = []
        for d in self._data["data"]["days"]:
            forecasts.append(
                Forecast(
                    datetime=ms_to_datetime(d["start"]),
                    temperature=d["temperature_max"],
                    templow=d["temperature_min"],
                    precipitation=d["rain"],
                    precipitation_probability=d["rain_probability"],
                    wind_speed=d["wind_speed"],
                    wind_gust_speed=d["wind_gust"],
                    condition=symbol_to_condition(d["symbol"]),
                )
            )
        return forecasts

