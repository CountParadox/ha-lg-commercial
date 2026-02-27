# LG Commercial Display (Direct IP) – Home Assistant Integration

Custom Home Assistant integration for controlling LG Commercial Displays over TCP (default port 9761) using the standard LG RS232/IP command set.

---

## Features

- Power control (with Wake-On-LAN)
- Input selection (installer-selectable)
- Volume control
- Mute control
- Channel (LCN) selection
- Raw command service
- Multi-device support
- Alternate command set toggle
- Regular polling for remote state changes

---

## IMPORTANT – Input Selection Required

During setup, you must manually select which inputs exist on your display.

LG commercial displays **do not provide a reliable method to query all available inputs over IP**.  
While it is possible to query the *current* input, the display does not expose a complete list of supported inputs.

Because of this limitation, the integration cannot automatically detect:

- Which HDMI ports exist
- Whether DisplayPort is available
- Whether OPS is installed
- Whether DTV is enabled
- Whether AV/Component inputs are present

You must select the correct inputs during configuration to match your specific model.

If you select an input that does not exist on the panel, the command will be sent but the display may ignore it.

---

## Determining Available Inputs

You can determine valid inputs by:

1. Checking the physical rear panel of the display
2. Reviewing the LG model specification sheet
3. Opening the on-screen input list menu on the display
4. Testing manually using the raw command service

---

## Accessing the Installer Menu

To enable network control and Wake-On-LAN:

1. Hold the INPUT button on the remote
2. Wait until the current input appears on screen
3. Press:

1105 ENTER

Inside the installer menu, enable:

- Network Ready
- Wake-On-LAN
- Mobile TV On (if available)
- Power On Status = Last

---

## Services

### Send Raw Command

Send arbitrary RS232/IP command (without carriage return).

Example:
lg_commercial.send_raw_command command: "ka 01 01"
---

### Set Channel (LCN)

Change to a digital channel by logical channel number.

Example:
lg_commercial.set_lcn lcn: 7
---

## Notes for Installers

- Default control port is 9761
- Set ID defaults to 01
- Some hospitality firmware may require the alternate command set toggle
- Polling interval is 20 seconds
- If the display becomes unreachable, it will show as unavailable in Home Assistant

---

This integration is designed for professional AV deployments where direct IP control is preferred over webOS control.
