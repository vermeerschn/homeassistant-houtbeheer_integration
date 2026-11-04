"""Vuldatum per houthok, zonder tijd."""
from datetime import date
from homeassistant.components.date import DateEntity
from .entity import WoodEntity

async def async_setup_entry(hass, entry, async_add_entities):
    store = hass.data["houtbeheer"][entry.entry_id]
    async_add_entities([FilledDateEntity(store, n) for n in range(1, store.shed_count + 1)])

class FilledDateEntity(WoodEntity, DateEntity):
    _attr_icon = "mdi:calendar"
    def __init__(self, store, number):
        super().__init__(store, number)
        self._attr_name = "Vuldatum"
        self._attr_unique_id = f"houtbeheer_{number}_filled_date"
    @property
    def native_value(self):
        value = self.store.shed(self.number).get("filled_date")
        if not value:
            return None
        try:
            return date.fromisoformat(value)
        except (ValueError, TypeError):
            return None
    async def async_set_value(self, value: date):
        await self.store.async_set(self.number, "filled_date", value.isoformat())
