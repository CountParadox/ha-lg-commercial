import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_IP_ADDRESS, CONF_PORT
from homeassistant.helpers import selector

from .const import (
    AVAILABLE_INPUTS,
    CONF_ENABLED_INPUTS,
    CONF_SET_ID,
    CONF_USE_ALTERNATE,
    CONF_WOL_ENTITY,
    DEFAULT_PORT,
    DOMAIN,
    LG_DEFAULT_SET_ID,
)


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
                vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
                vol.Optional(CONF_WOL_ENTITY): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain=["switch", "button"])
                ),
                vol.Optional(CONF_SET_ID, default=LG_DEFAULT_SET_ID): vol.Match(r"^\d{2}$"),
                vol.Optional(CONF_USE_ALTERNATE, default=False): bool,
                vol.Optional(CONF_ENABLED_INPUTS, default=list(AVAILABLE_INPUTS.keys())): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=list(AVAILABLE_INPUTS.keys()),
                        multiple=True,
                    )
                ),
            }),
        )
