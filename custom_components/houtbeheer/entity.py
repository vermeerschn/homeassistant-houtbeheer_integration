"""Gedeelde entity-code."""
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from .const import DOMAIN

class WoodEntity(Entity):
    _attr_has_entity_name = True
    def __init__(self, store, number: int) -> None:
        self.store = store
        self.number = number
        self._attr_device_info = DeviceInfo(identifiers={(DOMAIN, f"shed_{number}")}, name=f"Houthok {number}", manufacturer="Houtbeheer", model="Handmatige houtopslag")
    @property
    def extra_state_attributes(self):
        roles = {
            "WoodTypeSelect": "houtsoort",
            "DraftMoistureNumber": "invoer",
            "SaveMeasurementButton": "opslaan",
            "ResetShedButton": "reset",
            "MoistureSensor": "vocht",
            "LastMeasurementSensor": "datum",
            "ReadyToBurnSensor": "stookklaar",
            "ActiveShedSwitch": "actief",
            "FilledDateEntity": "vuldatum",
        }
        return {
            "houtbeheer_hok": self.number,
            "houtbeheer_id": f"{self.store.entry.entry_id}:shed_{self.number}",
            "houtbeheer_rol": roles[type(self).__name__],
        }

    async def async_added_to_hass(self):
        self.async_on_remove(self.store.async_add_listener(self.async_write_ha_state))
