"""Houtbeheer-integratie."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from .const import DOMAIN, PLATFORMS
from .store import WoodStore

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

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    store = WoodStore(hass, entry)
    await store.async_load()
    _async_remove_stale_sheds(hass, entry, store.shed_count)
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
