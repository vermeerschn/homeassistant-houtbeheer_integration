"""Configuratie voor Houtbeheer."""
from __future__ import annotations
from typing import Any
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from .const import CONF_SHEDS, DEFAULT_SHEDS, DOMAIN

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
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        current = self._entry.options.get(CONF_SHEDS, self._entry.data.get(CONF_SHEDS, DEFAULT_SHEDS))
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({vol.Required(CONF_SHEDS, default=current): vol.All(vol.Coerce(int), vol.Range(min=1, max=50))}),
        )
