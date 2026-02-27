import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_IP_ADDRESS, CONF_PORT, CONF_MAC
from homeassistant.helpers import selector

from .const import DOMAIN, DEFAULT_PORT, CONF_USE_ALTERNATE

AVAILABLE_INPUTS = {
    "DTV": "00",
    "HDMI1": "90",
    "HDMI2": "91",
    "HDMI3": "92",
    "HDMI4": "93",
    "DisplayPort": "C0",
    "OPS": "A0",
    "AV": "20",
    "Component": "40",
}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            self._base_config = user_input
            return await self.async_step_inputs()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME): str,
                vol.Required(CONF_IP_ADDRESS): str,
                vol.Required(CONF_MAC): str,
                vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
                vol.Optional(CONF_USE_ALTERNATE, default=False): bool,
                vol.Optional("set_id", default="01"): str,
            }),
        )

    async def async_step_inputs(self, user_input=None):
        if user_input is not None:
            data = {**self._base_config}
            data["enabled_inputs"] = user_input["enabled_inputs"]
            return self.async_create_entry(
                title=self._base_config[CONF_NAME],
                data=data,
            )

        return self.async_show_form(
            step_id="inputs",
            data_schema=vol.Schema({
                vol.Required("enabled_inputs"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=list(AVAILABLE_INPUTS.keys()),
                        multiple=True,
                    )
                )
            }),
        )
