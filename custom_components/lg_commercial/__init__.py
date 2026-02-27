import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType
from homeassistant.const import Platform

from .const import DOMAIN
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
        
        use_alternate=entry.data.get("use_alternate", False),
        set_id=entry.data.get("set_id", "01"),
    )

    coordinator = LGCoordinator(hass, api)
    coordinator.config_entry = entry
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register services once
    if not hass.services.has_service(DOMAIN, "send_raw_command"):

        async def handle_raw(call: ServiceCall):
            command = call.data["command"]
            entry_id = call.data.get("entry_id")
            if entry_id in hass.data[DOMAIN]:
                await hass.data[DOMAIN][entry_id].api.send(command)

        async def handle_lcn(call: ServiceCall):
            lcn = call.data["lcn"]
            entry_id = call.data.get("entry_id")
            if entry_id in hass.data[DOMAIN]:
                await hass.data[DOMAIN][entry_id].api.set_lcn(int(lcn))

        hass.services.async_register(DOMAIN, "send_raw_command", handle_raw)
        hass.services.async_register(DOMAIN, "set_lcn", handle_lcn)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
