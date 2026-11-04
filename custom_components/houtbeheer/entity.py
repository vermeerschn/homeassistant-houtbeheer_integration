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
    async def async_added_to_hass(self):
        self.async_on_remove(self.store.async_add_listener(self.async_write_ha_state))
