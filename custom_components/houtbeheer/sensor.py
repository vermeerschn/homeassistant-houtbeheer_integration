from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from .entity import WoodEntity
async def async_setup_entry(hass, entry, async_add_entities):
    store = hass.data["houtbeheer"][entry.entry_id]
    entities = []
    for n in range(1, store.shed_count + 1): entities += [MoistureSensor(store, n), LastMeasurementSensor(store, n)]
    async_add_entities(entities)
class MoistureSensor(WoodEntity, SensorEntity):
    _attr_native_unit_of_measurement = "%"; _attr_icon = "mdi:water-percent"
    def __init__(self, store, number): super().__init__(store, number); self._attr_name = "Opgeslagen vochtgehalte"; self._attr_unique_id = f"houtbeheer_{number}_moisture"
    @property
    def native_value(self): return self.store.shed(self.number)["moisture"]
class LastMeasurementSensor(WoodEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    def __init__(self, store, number): super().__init__(store, number); self._attr_name = "Laatste meting"; self._attr_unique_id = f"houtbeheer_{number}_last_measurement"
    @property
    def native_value(self):
        from homeassistant.util import dt as dt_util
        value = self.store.shed(self.number)["last_measurement"]
        return dt_util.parse_datetime(value) if value else None
class CustomWoodTypeSensor(WoodEntity, SensorEntity):
    _attr_icon = "mdi:tree-outline"
    def __init__(self, store, number): super().__init__(store, number); self._attr_name = "Eigen houtsoort"; self._attr_unique_id = f"houtbeheer_{number}_custom_wood_type"
    @property
    def native_value(self): return self.store.shed(self.number)["custom_wood_type"] or "Niet ingesteld"
