"""Lokale opslag voor Houtbeheer."""
from __future__ import annotations
from datetime import datetime
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers.storage import Store
from .const import DOMAIN, STORAGE_VERSION, WOOD_TYPES

def _empty_shed() -> dict:
    """Een leeg hok; gedeeld door nieuwe hokken en reset, zodat ze nooit uiteenlopen."""
    return {
        "wood_types": [],
        "draft_moisture": None,
        "moisture": None,
        "last_measurement": None,
        "active": False,
        "filled_date": None,
    }

def _normalize_wood_types(wood_types) -> list[str]:
    """Alleen bekende houtsoorten, zonder dubbels en altijd in dezelfde volgorde."""
    chosen = set(wood_types or [])
    return [wood for wood in WOOD_TYPES if wood in chosen]

class WoodStore:
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry
        self._store = Store(hass, STORAGE_VERSION, f"{DOMAIN}.{entry.entry_id}")
        self.data: dict = {"sheds": {}}
        self._listeners = []

    async def async_load(self) -> None:
        saved = await self._store.async_load()
        if saved:
            self.data = saved
        self._ensure_sheds()

    def _ensure_sheds(self) -> None:
        count = int(self.entry.options.get("sheds", self.entry.data.get("sheds", 12)))
        sheds = self.data.setdefault("sheds", {})
        for number in range(1, count + 1):
            sheds.setdefault(str(number), _empty_shed())
        for shed in sheds.values():
            shed.pop("custom_wood_type", None)
            shed.setdefault("active", False)
            shed.setdefault("filled_date", None)
            if "wood_types" not in shed:
                # Migratie vanaf versie 1.4.1 en ouder: één houtsoort als tekst wordt een lijst.
                # "Geen houtsoort" is geen houtsoort en wordt dus een lege lijst.
                shed["wood_types"] = _normalize_wood_types([shed.get("wood_type")])
            shed.pop("wood_type", None)

    @property
    def shed_count(self) -> int:
        return int(self.entry.options.get("sheds", self.entry.data.get("sheds", 12)))

    def shed(self, number: int) -> dict:
        return self.data["sheds"][str(number)]

    async def async_save(self) -> None:
        await self._store.async_save(self.data)
        for listener in self._listeners:
            listener()

    async def async_set(self, number: int, key: str, value) -> None:
        self.shed(number)[key] = value
        await self.async_save()

    async def async_set_wood_types(self, number: int, wood_types: list[str]) -> None:
        self.shed(number)["wood_types"] = _normalize_wood_types(wood_types)
        await self.async_save()

    async def async_save_measurement(self, number: int) -> None:
        shed = self.shed(number)
        if shed["draft_moisture"] is None:
            raise ServiceValidationError(
                f"Houthok {number}: vul eerst een nieuwe vochtmeting in voordat je de meting opslaat."
            )
        shed["moisture"] = shed["draft_moisture"]
        shed["last_measurement"] = datetime.now().astimezone().isoformat()
        await self.async_save()

    async def async_reset_shed(self, number: int) -> None:
        self.shed(number).update(_empty_shed())
        await self.async_save()

    @callback
    def async_add_listener(self, listener):
        self._listeners.append(listener)
        def remove_listener():
            self._listeners.remove(listener)
        return remove_listener
