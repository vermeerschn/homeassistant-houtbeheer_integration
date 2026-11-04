from homeassistant.components.select import SelectEntity
from .const import WOOD_TYPES
from .entity import WoodEntity
async def async_setup_entry(hass, entry, async_add_entities):
    store = hass.data["houtbeheer"][entry.entry_id]
    async_add_entities([WoodTypeSelect(store, n) for n in range(1, store.shed_count + 1)])
class WoodTypeSelect(WoodEntity, SelectEntity):
    _attr_options = WOOD_TYPES
    _attr_icon = "mdi:tree"
    def __init__(self, store, number):
        super().__init__(store, number); self._attr_name = "Houtsoort"; self._attr_unique_id = f"houtbeheer_{number}_wood_type"
    @property
    def current_option(self): return self.store.shed(self.number)["wood_type"]
    async def async_select_option(self, option): await self.store.async_set(self.number, "wood_type", option)
