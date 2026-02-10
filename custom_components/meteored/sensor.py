from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SensorEntity] = []

    data = coordinator.data or {}

    # ---------- HOURLY ----------
    hourly = data.get("hourly", {}).get("data", {}).get("hours", [])
    for idx, hour in enumerate(hourly):
        entities.extend(
            [
                MeteoredHourlySensor(coordinator, entry, idx, hour, "temperature", "Temperature", "°C"),
                MeteoredHourlySensor(coordinator, entry, idx, hour, "humidity", "Humidity", "%"),
                MeteoredHourlySensor(coordinator, entry, idx, hour, "wind_speed", "Wind Speed", "km/h"),
                MeteoredHourlySensor(coordinator, entry, idx, hour, "rain", "Rain", "mm"),
                MeteoredHourlySensor(coordinator, entry, idx, hour, "symbol", "Weather Symbol", None),
            ]
        )

    # ---------- DAILY ----------
    daily = data.get("daily", {}).get("data", {}).get("days", [])
    for idx, day in enumerate(daily):
        entities.extend(
            [
                MeteoredDailySensor(coordinator, entry, idx, day, "temperature_max", "Max Temperature", "°C"),
                MeteoredDailySensor(coordinator, entry, idx, day, "temperature_min", "Min Temperature", "°C"),
                MeteoredDailySensor(coordinator, entry, idx, day, "humidity", "Humidity", "%"),
                MeteoredDailySensor(coordinator, entry, idx, day, "wind_speed", "Wind Speed", "km/h"),
                MeteoredDailySensor(coordinator, entry, idx, day, "rain", "Rain", "mm"),
                MeteoredDailySensor(coordinator, entry, idx, day, "symbol", "Weather Symbol", None),
            ]
        )

    async_add_entities(entities)


# =========================
# ===== HOURLY SENSOR =====
# =========================
class MeteoredHourlySensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry, index: int, data: dict, key: str, label: str, unit: str | None):
        super().__init__(coordinator)

        self._data = data
        self._key = key
        self._index = index

        self._attr_unique_id = f"{entry.entry_id}_hourly_{key}_{index}"
        self._attr_name = f"Meteored Hour {index} {label}"
        self._attr_native_unit_of_measurement = unit

    @property
    def native_value(self):
        return self._data.get(self._key)


# ========================
# ===== DAILY SENSOR =====
# ========================
class MeteoredDailySensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry, index: int, data: dict, key: str, label: str, unit: str | None):
        super().__init__(coordinator)

        self._data = data
        self._key = key
        self._index = index

        self._attr_unique_id = f"{entry.entry_id}_daily_{key}_{index}"
        self._attr_name = f"Meteored Day {index} {label}"
        self._attr_native_unit_of_measurement = unit

    @property
    def native_value(self):
        return self._data.get(self._key)
