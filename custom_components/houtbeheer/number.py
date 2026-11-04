from homeassistant.components.number import NumberEntity, NumberMode
from .entity import WoodEntity
async def async_setup_entry(hass, entry, async_add_entities):
    store = hass.data["houtbeheer"][entry.entry_id]
    async_add_entities([DraftMoistureNumber(store, n) for n in range(1, store.shed_count + 1)])
class DraftMoistureNumber(WoodEntity, NumberEntity):
    _attr_native_min_value = 0; _attr_native_max_value = 100; _attr_native_step = 0.1; _attr_native_unit_of_measurement = "%"; _attr_mode = NumberMode.BOX; _attr_icon = "mdi:water-percent"
    def __init__(self, store, number):
        super().__init__(store, number); self._attr_name = "Nieuwe vochtmeting"; self._attr_unique_id = f"houtbeheer_{number}_draft_moisture"
    @property
    def native_value(self): return self.store.shed(self.number)["draft_moisture"]
    async def async_set_native_value(self, value): await self.store.async_set(self.number, "draft_moisture", value)
