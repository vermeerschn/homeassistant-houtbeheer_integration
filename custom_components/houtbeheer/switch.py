"""Hokken aanwijzen waaruit hout genomen mag worden."""
from homeassistant.components.switch import SwitchEntity
from .entity import WoodEntity

async def async_setup_entry(hass, entry, async_add_entities):
    store = hass.data["houtbeheer"][entry.entry_id]
    async_add_entities([ActiveShedSwitch(store, n) for n in range(1, store.shed_count + 1)])

class ActiveShedSwitch(WoodEntity, SwitchEntity):
    _attr_icon = "mdi:hand-pointing-right"
    def __init__(self, store, number):
        super().__init__(store, number)
        self._attr_name = "Actief hok"
        self._attr_unique_id = f"houtbeheer_{number}_active"
    @property
    def is_on(self):
        return self.store.shed(self.number).get("active", False)
    async def async_turn_on(self, **kwargs):
        await self.store.async_set(self.number, "active", True)
    async def async_turn_off(self, **kwargs):
        await self.store.async_set(self.number, "active", False)
