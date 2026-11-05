"""Configuratie voor Houtbeheer."""
from __future__ import annotations
from typing import Any
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import SelectSelector, SelectSelectorConfig, SelectSelectorMode
from .const import (
    CONF_SHEDS, CONF_WOOD_TYPES, DEFAULT_SHEDS, DEFAULT_WOOD_TYPES, DOMAIN,
    MAX_WOOD_NAME_LENGTH, MAX_WOOD_TYPES, NO_WOOD_TYPE,
)

def clean_wood_types(values) -> list[str] | None:
    """Spaties weg, lege waarden en dubbels (zonder op hoofdletters te letten) eruit.

    Geeft None terug als de lijst niet bruikbaar is.
    """
    cleaned: list[str] = []
    seen: set[str] = set()
    for value in values or []:
        name = " ".join(str(value).split())
        if not name or name.casefold() in seen:
            continue
        # Een komma is de scheiding in de leesbare status; "Geen houtsoort" is al de weergave voor leeg.
        if "," in name or len(name) > MAX_WOOD_NAME_LENGTH or name.casefold() == NO_WOOD_TYPE.casefold():
            return None
        seen.add(name.casefold())
        cleaned.append(name)
    return cleaned if 1 <= len(cleaned) <= MAX_WOOD_TYPES else None

def format_in_use(in_use: dict[str, list[int]], removed: list[str]) -> str:
    return "; ".join(f"{wood} (hok {', '.join(map(str, in_use[wood]))})" for wood in removed)

class HoutbeheerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        if user_input is not None:
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title="Houtbeheer", data=user_input)
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_SHEDS, default=DEFAULT_SHEDS): vol.All(vol.Coerce(int), vol.Range(min=1, max=50))}),
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        return HoutbeheerOptionsFlow(config_entry)

class HoutbeheerOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self._entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        current_sheds = self._entry.options.get(CONF_SHEDS, self._entry.data.get(CONF_SHEDS, DEFAULT_SHEDS))
        current_woods = list(self._entry.options.get(CONF_WOOD_TYPES, DEFAULT_WOOD_TYPES))
        errors: dict[str, str] = {}
        placeholders = {"in_use": ""}
        offered = current_woods
        if user_input is not None:
            woods = clean_wood_types(user_input.get(CONF_WOOD_TYPES))
            if woods is None:
                errors[CONF_WOOD_TYPES] = "wood_types_invalid"
                offered = list(user_input.get(CONF_WOOD_TYPES) or current_woods)
            else:
                store = self.hass.data.get(DOMAIN, {}).get(self._entry.entry_id)
                in_use = store.wood_types_in_use() if store else {}
                # Volgorde van de huidige lijst; soorten die er niet meer in staan komen achteraan.
                known = [*current_woods, *(wood for wood in in_use if wood not in current_woods)]
                removed = [wood for wood in known if wood in in_use and wood not in woods]
                if removed:
                    errors[CONF_WOOD_TYPES] = "wood_types_in_use"
                    placeholders["in_use"] = format_in_use(in_use, removed)
                    offered = list(user_input[CONF_WOOD_TYPES])
                else:
                    return self.async_create_entry(
                        title="", data={CONF_SHEDS: user_input[CONF_SHEDS], CONF_WOOD_TYPES: woods}
                    )
        sheds = user_input[CONF_SHEDS] if user_input else current_sheds
        options = list(dict.fromkeys([*offered, *current_woods]))
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_SHEDS, default=sheds): vol.All(vol.Coerce(int), vol.Range(min=1, max=50)),
                vol.Required(CONF_WOOD_TYPES, default=offered): SelectSelector(SelectSelectorConfig(
                    options=options, multiple=True, custom_value=True, mode=SelectSelectorMode.DROPDOWN,
                )),
            }),
            errors=errors,
            description_placeholders=placeholders,
        )
