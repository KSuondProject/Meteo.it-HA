from homeassistant.components.weather import WeatherEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, SYMBOLS_MAP

async def async_setup_entry(hass, entry, coordinator):
    await hass.helpers.entity_platform.async_add_entities([MeteoredWeather(coordinator)])

class MeteoredWeather(CoordinatorEntity, WeatherEntity):
    """Weather entity Meteored."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Meteored Weather"
        self._attr_unique_id = "meteored_weather"

    @property
    def condition(self):
        """Condizione principale del giorno (dal daily sensor)"""
        hours = self._get_hours()
        if not hours:
            return None
        symbols = [h.get("symbol") for h in hours if h.get("symbol") is not None]
        if not symbols:
            return None
        symbol = max(set(symbols), key=symbols.count)
        return SYMBOLS_MAP.get(symbol, "unknown")

    @property
    def temperature(self):
        hours = self._get_hours()
        temps = [h.get("temperature") for h in hours if h.get("temperature") is not None]
        return round(sum(temps)/len(temps), 1) if temps else None

    @property
    def forecast(self):
        """Puoi aggiungere forecast per 24h se vuoi"""
        return []

    def _get_hours(self):
        data = self.coordinator.data
        if not data:
            return []
        return data.get("data", {}).get("hours", [])
