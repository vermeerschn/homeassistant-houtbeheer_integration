"""Stookklaar: het opgeslagen vochtpercentage zit onder de ingestelde grens."""
from homeassistant.components.binary_sensor import BinarySensorEntity
from .const import ATTR_READY_THRESHOLD
from .entity import WoodEntity

async def async_setup_entry(hass, entry, async_add_entities):
    store = hass.data["houtbeheer"][entry.entry_id]
    async_add_entities([ReadyToBurnSensor(store, n) for n in range(1, store.shed_count + 1)])

class ReadyToBurnSensor(WoodEntity, BinarySensorEntity):
    _attr_icon = "mdi:fire"
    def __init__(self, store, number):
        super().__init__(store, number)
        self._attr_name = "Stookklaar"
        self._attr_unique_id = f"houtbeheer_{number}_ready"
    @property
    def is_on(self):
        moisture = self.store.shed(self.number)["moisture"]
        return moisture is not None and moisture < self.store.ready_threshold
    @property
    def extra_state_attributes(self):
        # De kaart leest de grens hier, zodat ze op één plek ingesteld wordt.
        return {**super().extra_state_attributes, ATTR_READY_THRESHOLD: self.store.ready_threshold}
