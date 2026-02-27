# LG Commercial Display (Direct IP) - Home Assistant Integration

Custom integration for controlling LG Commercial Displays over TCP (default port 9761).

## Features

- Power control (with Wake-On-LAN)
- Input selection
- Volume & mute
- Channel (LCN) selection
- Raw command service
- Multi-device support
- Alternate command set toggle
- ARP auto-discovery
- Regular polling for remote state changes

## Enabling Network Control on LG Displays

1. Hold INPUT until current input appears
2. Press: 1105 ENTER
3. Enable:
   - Network Ready
   - Wake-On-LAN
   - Mobile TV On
   - Power On Status = Last
