# Security Integration Plugin

The `security_status_plugin.py` enables the Cyberdeck to display real-time status from Security Research tools.

## Overview

When security tools (WiFi scanner, OpSec verification, Nmap, etc.) are running, this plugin:

1. Reads status from `/tmp/cyberdeck_status.json`
2. Controls LED colors based on the operation mode
3. Takes over the OLED display to show operation details

## LED Mode Mapping

| Security Mode | LED Color | Effect | Description |
|---------------|-----------|--------|-------------|
| `idle` | Rainbow | Fade/breathing | No security operation active |
| `wifi_scan` | Red | Breathing | WiFi scanning in progress |
| `monitor` | Purple | Pulse | Monitor mode enabled |
| `recon` | Yellow | Breathing | Reconnaissance/OSINT |
| `scanning` | Blue | Pulse | Network scanning (Nmap) |
| `exploit` | Orange | Strobe | Exploitation phase |
| `alert` | Red | Fast flash | Error or critical event |
| `safe` | Green | Solid | OpSec verified, identity safe |

## OLED Display

When a security mode is active (not `idle`), the OLED shows a dedicated security screen:

```
┌────────────────────┐
│ [PHASE NAME]       │  ← Current operation phase
│ TGT: target_value  │  ← Target (IP, interface, etc.)
│ ████████░░░░░░ 53% │  ← Progress bar
│ Status message     │  ← Status or details
└────────────────────┘
```

The normal 3-screen rotation (System, Date/Time, Temperature) resumes when the security mode returns to `idle`.

## Files

| File | Purpose |
|------|---------|
| `plugins/security_status_plugin.py` | Main plugin - reads status, controls LEDs |
| `plugins/oled_display_plugin.py` | Updated - adds security screen rendering |
| `plugin_loader.py` | Updated - loads security_status_plugin |

## Status File Format

The plugin reads from `/tmp/cyberdeck_status.json`:

```json
{
  "mode": "wifi_scan",
  "phase": "WiFi Scan",
  "target": "wlan1",
  "progress": 50,
  "progress_max": 100,
  "message": "APs: 12 | Clients: 5",
  "details": {
    "channel": 6
  },
  "timestamp": "2026-01-31T14:30:00"
}
```

## Integration with Security Research

This plugin works with tools from the Security Research repository that use the `hardware_bridge.py` module:

- `02-OpSec/verify_identity.py` - Identity verification
- `02-OpSec/stealth_mode.py` - MAC randomization, stealth setup
- `04-Scanning/tools/wifi_scanner.py` - WiFi network scanning

See `Security_Research/13-Utils/HARDWARE_BRIDGE.md` for the full API documentation.

## Testing

Run the Cyberdeck daemon and use the test script:

**Terminal 1:**
```bash
cd /home/cowboy/Documents/projects/git/Cyberdeck/Code
python application.py
```

**Terminal 2:**
```bash
cd /home/cowboy/Documents/projects/git/Security_Research/13-Utils
python test_hardware_bridge.py --demo
```

Watch the LEDs cycle through all security modes.
