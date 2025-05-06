from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import TextSelector, TextSelectorConfig

from .const import DOMAIN, DEFAULT_ZONE

DATA_SCHEMA = vol.Schema({
    vol.Required("username"): str,
    vol.Required("password"): str,
    vol.Required("nom", default=DEFAULT_ZONE["nom"]): str,
    vol.Required("code_zone", default=DEFAULT_ZONE["code_zone"]): str,
    vol.Required("codeEpci", default=DEFAULT_ZONE["codeEpci"]): str,
})

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Pollens France", data={
                "username": user_input["username"],
                "password": user_input["password"],
                "zone": {
                    "nom": user_input["nom"],
                    "code_zone": user_input["code_zone"],
                    "codeEpci": user_input["codeEpci"]
                }
            })

        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)

class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return self.async_show_form(step_id="init", data_schema=vol.Schema({}))