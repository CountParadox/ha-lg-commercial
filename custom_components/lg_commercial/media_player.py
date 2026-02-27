from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import MediaPlayerEntityFeature
from homeassistant.const import STATE_ON, STATE_OFF
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

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


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    enabled_inputs = entry.data.get("enabled_inputs", list(AVAILABLE_INPUTS.keys()))
    async_add_entities([
        LGCommercialMediaPlayer(coordinator, entry.title, enabled_inputs)
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

    def __init__(self, coordinator, name, enabled_inputs):
        super().__init__(coordinator)
        self._attr_unique_id = f"lg_commercial_{self.coordinator.api.host}"
        self._attr_name = name
        self._enabled_inputs = enabled_inputs

    @property
    def state(self):
        if self.coordinator.data and "01 OK" in self.coordinator.data.get("power", ""):
            return STATE_ON
        return STATE_OFF

    @property
    def source_list(self):
        return self._enabled_inputs

    async def async_turn_on(self):
        await self.coordinator.api.power_on(self.hass)

    async def async_turn_off(self):
        await self.coordinator.api.power_off()

    async def async_select_source(self, source):
        code = AVAILABLE_INPUTS[source]
        await self.coordinator.api.set_input(code)

    async def async_set_volume_level(self, volume):
        await self.coordinator.api.set_volume(int(volume * 100))

    async def async_mute_volume(self, mute):
        await self.coordinator.api.set_mute(mute)
