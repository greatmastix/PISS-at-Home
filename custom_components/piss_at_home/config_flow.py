from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    DEFAULT_OPTIONS,
    DOMAIN,
    OPTION_INCLUDE_FRESH_WATER_TANK,
    OPTION_INCLUDE_URINE_TANK,
    OPTION_INCLUDE_WASTE_WATER_TANK,
)


class PissatHomeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for PISS@Home."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        # No user inputs required — create a single instance.
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title="PISS@Home", data={})

    @callback
    def async_get_options_flow(self):
        return PissatHomeOptionsFlow


class PissatHomeOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = {**DEFAULT_OPTIONS, **self.config_entry.options}
        schema = vol.Schema(
            {
                vol.Optional(
                    OPTION_INCLUDE_URINE_TANK,
                    default=options[OPTION_INCLUDE_URINE_TANK],
                ): bool,
                vol.Optional(
                    OPTION_INCLUDE_WASTE_WATER_TANK,
                    default=options[OPTION_INCLUDE_WASTE_WATER_TANK],
                ): bool,
                vol.Optional(
                    OPTION_INCLUDE_FRESH_WATER_TANK,
                    default=options[OPTION_INCLUDE_FRESH_WATER_TANK],
                ): bool,
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
