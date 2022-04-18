from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from .const import CONF_ENABLE, CONF_PROXY, DOMAIN


class ProxyFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for HACS."""

    VERSION = 1

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input):
        """Handle a flow initialized by the user."""
        self._errors = {}
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        
        if user_input:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_ENABLE, default=True): bool,
                    vol.Required(CONF_PROXY, ): str,
                }
            ),
            errors=self._errors,
        )


    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return ProxyOptionsFlowHandler(config_entry)


class ProxyOptionsFlowHandler(config_entries.OptionsFlow):

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, _user_input=None):
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        self._errors = {}
        
        if user_input:
            self.hass.config_entries.async_update_entry(self.config_entry,data=user_input)
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_ENABLE, default=self.config_entry.data.get(CONF_ENABLE)): bool,
                    vol.Required(CONF_PROXY, default=self.config_entry.data.get(CONF_PROXY)): str,
                }
            ),
            errors=self._errors,
        )
