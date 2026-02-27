from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import MediaPlayerEntityFeature
from homeassistant.const import STATE_ON, STATE_OFF
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([LGCommercialMediaPlayer(coordinator, entry.title)])


class LGCommercialMediaPlayer(CoordinatorEntity, MediaPlayerEntity):

    _attr_supported_features = (
        MediaPlayerEntityFeature.TURN_ON
        | MediaPlayerEntityFeature.TURN_OFF
        | MediaPlayerEntityFeature.SELECT_SOURCE
        | MediaPlayerEntityFeature.VOLUME_SET
        | MediaPlayerEntityFeature.VOLUME_STEP
        | MediaPlayerEntityFeature.VOLUME_MUTE
    )

    def __init__(self, coordinator, name):
        super().__init__(coordinator)
        self._attr_name = name

        self._sources = {
            "HDMI1": "90",
            "HDMI2": "91",
            "DTV": "00",
        }

    @property
    def state(self):
        if "01 OK" in self.coordinator.data["power"]:
            return STATE_ON
        return STATE_OFF

    @property
    def source_list(self):
        return list(self._sources.keys())

    async def async_turn_on(self):
        await self.coordinator.api.power_on()

    async def async_turn_off(self):
        await self.coordinator.api.power_off()

    async def async_select_source(self, source):
        code = self._sources[source]
        await self.coordinator.api.set_input(code)

    async def async_set_volume_level(self, volume):
        await self.coordinator.api.set_volume(int(volume * 100))

    async def async_mute_volume(self, mute):
        await self.coordinator.api.set_mute(mute)
