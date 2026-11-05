from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from .const import ATTR_MEASUREMENTS, ATTR_WOOD_OPTIONS, ATTR_WOOD_TYPES, NO_WOOD_TYPE, WOOD_TYPES
from .entity import WoodEntity
async def async_setup_entry(hass, entry, async_add_entities):
    store = hass.data["houtbeheer"][entry.entry_id]
    entities = []
    for n in range(1, store.shed_count + 1): entities += [WoodTypesSensor(store, n), MoistureSensor(store, n), LastMeasurementSensor(store, n)]
    async_add_entities(entities)
class MoistureSensor(WoodEntity, SensorEntity):
    _attr_native_unit_of_measurement = "%"; _attr_icon = "mdi:water-percent"
    # MEASUREMENT zorgt voor long-term statistics, zodat de droogcurve per hok bewaard blijft.
    _attr_state_class = SensorStateClass.MEASUREMENT
    # De lijst met metingen is voor de kaart; de recorder bewaart de waarde zelf al als statistiek.
    _unrecorded_attributes = frozenset({ATTR_MEASUREMENTS})
    def __init__(self, store, number): super().__init__(store, number); self._attr_name = "Opgeslagen vochtgehalte"; self._attr_unique_id = f"houtbeheer_{number}_moisture"
    @property
    def native_value(self): return self.store.shed(self.number)["moisture"]
    @property
    def extra_state_attributes(self):
        return {
            **super().extra_state_attributes,
            ATTR_MEASUREMENTS: [
                {"datum": item["date"], "vocht": item["moisture"]}
                for item in self.store.shed(self.number)["history"]
            ],
        }
class LastMeasurementSensor(WoodEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    def __init__(self, store, number): super().__init__(store, number); self._attr_name = "Laatste meting"; self._attr_unique_id = f"houtbeheer_{number}_last_measurement"
    @property
    def native_value(self):
        from homeassistant.util import dt as dt_util
        value = self.store.shed(self.number)["last_measurement"]
        return dt_util.parse_datetime(value) if value else None
class WoodTypesSensor(WoodEntity, SensorEntity):
    """Houtsoorten in dit hok: de state is leesbaar, de lijst zit in het attribuut houtsoorten."""
    _attr_icon = "mdi:tree"
    # De lijst met opties is voor de kaart en hoeft niet in de recorder.
    _unrecorded_attributes = frozenset({ATTR_WOOD_OPTIONS})
    def __init__(self, store, number): super().__init__(store, number); self._attr_name = "Houtsoorten"; self._attr_unique_id = f"houtbeheer_{number}_wood_types"
    @property
    def native_value(self):
        types = self.store.shed(self.number)["wood_types"]
        return ", ".join(types) if types else NO_WOOD_TYPE
    @property
    def extra_state_attributes(self):
        return {
            **super().extra_state_attributes,
            ATTR_WOOD_TYPES: list(self.store.shed(self.number)["wood_types"]),
            ATTR_WOOD_OPTIONS: list(WOOD_TYPES),
        }

