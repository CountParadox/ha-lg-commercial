# LG Commercial Display (Direct IP) - Home Assistant Integration

Custom Home Assistant integration for controlling LG Commercial Displays over TCP (default port `9761`) using the LG RS232/IP command set.

## Features

- Power control (with optional Wake-on-LAN helper entity)
- Input selection (installer-selectable)
- Volume set, mute, volume up/down
- Channel (LCN) selection service
- Raw command service
- Multi-device support
- Alternate input command set toggle (`xb` vs `xv`)
- Regular polling for remote state changes

## Configuration

The config flow exposes:

- `Name`
- `IP address`
- `Port` (default `9761`)
- `Wake-on-LAN entity` (`switch` or `button`, optional)
- `Set ID` (2 digits, default `01`)
- `Use alternate input command set` (optional)
- `Enabled inputs` (multi-select)

### Important: Input Selection Is Manual

LG commercial displays do not provide a reliable API to enumerate all supported inputs over IP.  
You can query the current input, but not a complete per-model list.

Select only the inputs that exist on your panel. Invalid inputs may be ignored by the display.

## Services

### `lg_commercial.send_raw_command`

Send an arbitrary command (without trailing carriage return).

```yaml
service: lg_commercial.send_raw_command
data:
  command: "ka 01 01"
  entry_id: "01J123ABC456DEF789GH0IJKL"  # optional when only one device is configured
```

### `lg_commercial.set_lcn`

Set digital channel by logical channel number.

```yaml
service: lg_commercial.set_lcn
data:
  lcn: 7
  entry_id: "01J123ABC456DEF789GH0IJKL"  # optional when only one device is configured
```

If multiple LG entries are configured, `entry_id` is required for these services.

## Installer Notes

- Ensure network control is enabled on the display.
- Enable Wake-on-LAN/Network Ready options in installer menu when available.
- Polling interval is 20 seconds.
- If the display is unreachable, the entity becomes unavailable until communication recovers.

This integration is designed for professional AV deployments where direct IP control is preferred over webOS control.
