import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_IP_ADDRESS, CONF_PORT, CONF_MAC
from homeassistant.helpers import selector

from .const import DOMAIN, DEFAULT_PORT


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME): str,
                vol.Required(CONF_IP_ADDRESS): str,
                vol.Required(CONF_MAC): str,
                vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
                vol.Optional("wol_entity"): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain=["switch","button"])
                ),
            }),
        )
