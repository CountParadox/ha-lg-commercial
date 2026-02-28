DOMAIN = "lg_commercial"

DEFAULT_PORT = 9761
DEFAULT_SCAN_INTERVAL = 20
DEFAULT_COMMAND_TIMEOUT = 5

CONF_USE_ALTERNATE = "use_alternate"
CONF_SET_ID = "set_id"
CONF_WOL_ENTITY = "wol_entity"
CONF_ENABLED_INPUTS = "enabled_inputs"

LG_DEFAULT_SET_ID = "01"

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

# Known LG MAC prefixes for discovery
LG_OUIS = [
    "58:FD:B1",
    "00:1E:75",
    "A0:39:F7",
    "64:BC:0C"
]
