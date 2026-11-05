"""Houtbeheer-integratie."""
from __future__ import annotations

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv, device_registry as dr, entity_registry as er
from .const import DOMAIN, PLATFORMS, SERVICE_SET_WOOD_TYPES, WOOD_TYPES
from .store import WoodStore

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

SET_WOOD_TYPES_SCHEMA = vol.Schema({
    vol.Required("shed"): vol.All(vol.Coerce(int), vol.Range(min=1)),
    vol.Required("wood_types"): vol.All(cv.ensure_list, [vol.In(WOOD_TYPES)]),
})

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    async def async_set_wood_types(call: ServiceCall) -> None:
        stores = list(hass.data.get(DOMAIN, {}).values())
        if not stores:
            raise ServiceValidationError("Houtbeheer is niet geladen.")
        store, number = stores[0], call.data["shed"]
        if number > store.shed_count:
            raise ServiceValidationError(f"Houthok {number} bestaat niet; er zijn {store.shed_count} hokken.")
        await store.async_set_wood_types(number, call.data["wood_types"])

    hass.services.async_register(DOMAIN, SERVICE_SET_WOOD_TYPES, async_set_wood_types, schema=SET_WOOD_TYPES_SCHEMA)
    return True

def _async_remove_stale_sheds(hass: HomeAssistant, entry: ConfigEntry, shed_count: int) -> None:
    """Verwijder apparaten en entiteiten van hokken boven het ingestelde aantal.

    De opgeslagen hokdata blijft bewaard: verhoog je het aantal later weer,
    dan komen die hokken met hun oude gegevens terug.
    """
    registry = dr.async_get(hass)
    for device in dr.async_entries_for_config_entry(registry, entry.entry_id):
        for domain, identifier in device.identifiers:
            if domain != DOMAIN or not identifier.startswith("shed_"):
                continue
            try:
                number = int(identifier.removeprefix("shed_"))
            except ValueError:
                break
            if number > shed_count:
                registry.async_remove_device(device.id)
            break

def _async_remove_legacy_entities(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Verwijder de houtsoort-keuzelijsten (select) van versie 1.4.1 en ouder.

    Een select kent maar één waarde; ze zijn vervangen door de sensor Houtsoorten.
    """
    registry = er.async_get(hass)
    for entity in er.async_entries_for_config_entry(registry, entry.entry_id):
        if entity.domain == "select":
            registry.async_remove(entity.entity_id)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    store = WoodStore(hass, entry)
    await store.async_load()
    _async_remove_stale_sheds(hass, entry, store.shed_count)
    _async_remove_legacy_entities(hass, entry)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = store
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_options_updated))
    return True

async def async_options_updated(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unloaded
