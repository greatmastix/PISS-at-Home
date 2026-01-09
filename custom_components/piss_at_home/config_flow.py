from __future__ import annotations

from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN


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
        # No options yet; placeholder for future settings (e.g., reconnect backoff).
        return self.async_create_entry(title="", data={})
