from homeassistant.components.button import ButtonEntity
from .entity import WoodEntity
async def async_setup_entry(hass, entry, async_add_entities):
    store = hass.data["houtbeheer"][entry.entry_id]
    async_add_entities([
        entity
        for n in range(1, store.shed_count + 1)
        for entity in (SaveMeasurementButton(store, n), ResetShedButton(store, n))
    ])
class SaveMeasurementButton(WoodEntity, ButtonEntity):
    _attr_icon = "mdi:content-save-check"
    def __init__(self, store, number):
        super().__init__(store, number); self._attr_name = "Meting opslaan"; self._attr_unique_id = f"houtbeheer_{number}_save_measurement"
    async def async_press(self): await self.store.async_save_measurement(self.number)

class ResetShedButton(WoodEntity, ButtonEntity):
    _attr_icon = "mdi:delete-sweep-outline"
    def __init__(self, store, number):
        super().__init__(store, number)
        self._attr_name = "Reset hok"
        self._attr_unique_id = f"houtbeheer_{number}_reset"
    async def async_press(self):
        await self.store.async_reset_shed(self.number)
