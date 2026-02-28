import re

from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import MediaPlayerEntityFeature
from homeassistant.const import STATE_ON, STATE_OFF
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import AVAILABLE_INPUTS, CONF_ENABLED_INPUTS, CONF_WOL_ENTITY, DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    enabled_inputs = entry.data.get(CONF_ENABLED_INPUTS, list(AVAILABLE_INPUTS.keys()))
    code_to_name = {code.upper(): name for name, code in AVAILABLE_INPUTS.items()}
    normalized_inputs = []
    for value in enabled_inputs:
        if value in AVAILABLE_INPUTS:
            normalized_inputs.append(value)
            continue
        mapped_name = code_to_name.get(str(value).upper())
        if mapped_name:
            normalized_inputs.append(mapped_name)
    enabled_inputs = normalized_inputs
    if not enabled_inputs:
        enabled_inputs = list(AVAILABLE_INPUTS.keys())
    wol_entity = entry.data.get(CONF_WOL_ENTITY)
    async_add_entities([
        LGCommercialMediaPlayer(coordinator, entry.title, enabled_inputs, wol_entity)
    ])


class LGCommercialMediaPlayer(CoordinatorEntity, MediaPlayerEntity):

    _attr_supported_features = (
        MediaPlayerEntityFeature.TURN_ON
        | MediaPlayerEntityFeature.TURN_OFF
        | MediaPlayerEntityFeature.SELECT_SOURCE
        | MediaPlayerEntityFeature.VOLUME_SET
        | MediaPlayerEntityFeature.VOLUME_STEP
        | MediaPlayerEntityFeature.VOLUME_MUTE
    )

    def __init__(self, coordinator, name, enabled_inputs, wol_entity):
        super().__init__(coordinator)
        self._attr_unique_id = (
            f"lg_commercial_{self.coordinator.api.host}_"
            f"{self.coordinator.api.port}_{self.coordinator.api.set_id}"
        )
        self._attr_name = name
        self._enabled_inputs = enabled_inputs
        self._wol_entity = wol_entity

    def _extract_ok_value(self, key):
        if not self.coordinator.data:
            return None
        value = self.coordinator.data.get(key, "")
        match = re.search(r"\bOK([0-9A-Fa-f]{2,3})", value)
        if match:
            return match.group(1)
        return None

    @property
    def state(self):
        if self.coordinator.data and "01 OK" in self.coordinator.data.get("power", ""):
            return STATE_ON
        return STATE_OFF

    @property
    def volume_level(self):
        raw = self._extract_ok_value("volume")
        if raw is None:
            return None
        return min(1.0, max(0.0, int(raw, 16) / 100))

    @property
    def is_volume_muted(self):
        raw = self._extract_ok_value("mute")
        if raw is None:
            return None
        return raw == "01"

    @property
    def source_list(self):
        return self._enabled_inputs

    @property
    def source(self):
        raw = self._extract_ok_value("input")
        if raw is None:
            return None
        reverse_inputs = {code.upper(): name for name, code in AVAILABLE_INPUTS.items()}
        return reverse_inputs.get(raw.upper())

    async def async_turn_on(self):
        await self.coordinator.api.power_on(self.hass, self._wol_entity)

    async def async_turn_off(self):
        await self.coordinator.api.power_off()

    async def async_select_source(self, source):
        code = AVAILABLE_INPUTS.get(source)
        if code is None:
            raise HomeAssistantError(f"Unsupported source requested: {source}")
        await self.coordinator.api.set_input(code)
        await self.coordinator.async_request_refresh()

    async def async_set_volume_level(self, volume):
        await self.coordinator.api.set_volume(int(volume * 100))

    async def async_volume_up(self):
        current = self.volume_level if self.volume_level is not None else 0.5
        await self.async_set_volume_level(min(1.0, current + 0.05))

    async def async_volume_down(self):
        current = self.volume_level if self.volume_level is not None else 0.5
        await self.async_set_volume_level(max(0.0, current - 0.05))

    async def async_mute_volume(self, mute):
        await self.coordinator.api.set_mute(mute)
