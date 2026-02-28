import logging
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType
from homeassistant.const import Platform

from .const import CONF_SET_ID, CONF_USE_ALTERNATE, DOMAIN, LG_DEFAULT_SET_ID
from .coordinator import LGCoordinator, LGDisplayAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.MEDIA_PLAYER]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})

    api = LGDisplayAPI(
        host=entry.data["ip_address"],
        port=entry.data["port"],
        use_alternate=entry.data.get(CONF_USE_ALTERNATE, False),
        set_id=entry.data.get(CONF_SET_ID, LG_DEFAULT_SET_ID),
    )

    coordinator = LGCoordinator(hass, api)
    coordinator.config_entry = entry
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register services once
    if not hass.services.has_service(DOMAIN, "send_raw_command"):
        def _resolve_target_coordinator(entry_id):
            coordinators = hass.data[DOMAIN]
            if entry_id:
                if entry_id in coordinators:
                    return coordinators[entry_id]
                raise ServiceValidationError(f"Unknown entry_id: {entry_id}")

            if len(coordinators) == 1:
                return next(iter(coordinators.values()))

            raise ServiceValidationError(
                "Multiple LG displays configured. Please provide entry_id."
            )

        async def handle_raw(call: ServiceCall):
            command = call.data["command"]
            entry_id = call.data.get("entry_id")
            coordinator = _resolve_target_coordinator(entry_id)
            await coordinator.api.send(command)

        async def handle_lcn(call: ServiceCall):
            lcn = call.data["lcn"]
            entry_id = call.data.get("entry_id")
            coordinator = _resolve_target_coordinator(entry_id)
            await coordinator.api.set_lcn(int(lcn))

        hass.services.async_register(
            DOMAIN,
            "send_raw_command",
            handle_raw,
            schema=vol.Schema(
                {
                    vol.Required("command"): cv.string,
                    vol.Optional("entry_id"): cv.string,
                }
            ),
        )
        hass.services.async_register(
            DOMAIN,
            "set_lcn",
            handle_lcn,
            schema=vol.Schema(
                {
                    vol.Required("lcn"): vol.All(vol.Coerce(int), vol.Range(min=0, max=999)),
                    vol.Optional("entry_id"): cv.string,
                }
            ),
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        if not hass.data[DOMAIN]:
            hass.services.async_remove(DOMAIN, "send_raw_command")
            hass.services.async_remove(DOMAIN, "set_lcn")

    return unload_ok
