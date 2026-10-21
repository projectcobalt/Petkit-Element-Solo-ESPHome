# PETKIT Fresh Element Solo for ESPHome

Reusable ESPHome firmware and a Home Assistant automation blueprint for the
PETKIT Fresh Element Solo feeder, model D4-2 / product code P570.

This is an independent community project. It is not affiliated with or endorsed
by PETKIT.

Current release: `v2.0.0`

Version 2.0.0 includes device-owned food tracking and refill alerts.
Both feeders are configured; the update preserved their food settings and reserves.
Tracking and refill reminder timing run on the device using native ESPHome
globals, scripts, the RTC and event entities. Home Assistant forwards refill events.
See [food reserve setup and operation](docs/food-reserve.md)
for calibration, refill controls, consolidated alerts, persistence limits, and rollout checks.

## What This Project Provides

This project turns the Element Solo into a locally managed ESPHome feeder with
Home Assistant supervision. The firmware exposes the feeder hardware as normal
ESPHome entities, and the blueprint uses those entities to schedule feeds,
confirm outcomes, and notify when something needs attention.

Current project outcomes:

- Local feed control through ESPHome with configurable portion counts.
- Child Lock for ignoring accidental physical side-button feed requests.
- Feed completion events for completed, jammed, and rejected feed attempts.
- Home Assistant scheduling and supervision through a reusable blueprint.
- Food-drop pulse monitoring with a persistent Food State surface.
- Device-owned estimated reserve in grams, calibrated consumption totals,
  full refills and partial top-ups.
- Consolidated refill warnings, Brisbane 09:00 reminders, and reconnect recovery.
- Feeder State, Last Feed Portions, Food Drop Pulses, Battery Pack Voltage,
  Battery Pack Level, DC Input Voltage, Battery Power Active, and diagnostic
  restart information.
- Anti-jam handling, motor pulse lockout, and feed/reverse motor control.
- Status LED behavior for active feeding, Wi-Fi connected, and Wi-Fi
  disconnected states.
- Basic sound feedback through tunable RTTTL substitutions.
- A dormant deep-sleep foundation using the manual feed button as a wake pin.

## Install And Adoption

The reusable ESPHome package is:

```text
github://projectcobalt/petkit-element-solo/petkit-element-solo.yaml@v2.0.0
```

Raw configuration URL:

```text
https://raw.githubusercontent.com/projectcobalt/petkit-element-solo/main/petkit-element-solo.yaml
```

After flashing and provisioning, use **Take Control** in the ESPHome dashboard.
ESPHome will create an individual per-device YAML for future OTA updates. Keep
that adopted device YAML separate from this reusable factory package.

## Versions And Updates

Firmware package versions are tracked in the ESPHome project metadata and in
GitHub releases. Existing adopted ESPHome YAMLs that import the package from
`@main` will compile against the latest package content the next time they are
validated or built.

Home Assistant blueprints are different: Home Assistant does not automatically
replace an imported blueprint when the GitHub file changes. Re-import the
blueprint after repository updates, then reload automations.

## Home Assistant Blueprint

The included blueprint schedules feeds and supervises the result. It discovers
the feeder's ESPHome entities from a single device selector, sets Feed Portions,
presses Feed Now, waits for a new feeder event, and branches on the reported
event type.

It can notify for:

- Jams or rejected feeds.
- Unavailable feeder entities.
- Feed completion that reports the wrong portion count.
- Completed dry runs where no food-drop pulses were detected.
- Power-source warnings and low battery voltage.
- Optional successful feed confirmation.
- Device-owned low-food events and RTC-timed daily reminders, forwarded by HA.
- A distinct low-food completion tune that respects Mute Sounds.

[Import the blueprint into Home Assistant](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fprojectcobalt%2Fpetkit-element-solo%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Felement-solo-feeding.yaml)

## Hardware Findings

The project is based on community ESPHome work for the PETKIT Fresh Element
Solo and follow-up testing on a real feeder. The supported hardware exposes:

- Motor forward and reverse control.
- A cam or portion pulse input used to count dispensed portions.
- A food-drop sensor pulse input.
- Battery-pack and DC-input voltage sensing.
- Battery/DC power-source state.
- Manual feed and Wi-Fi/provisioning buttons.
- A status LED and piezo buzzer.

The firmware preserves these hardware surfaces in ESPHome so Home Assistant can
supervise feeding without relying on the original PETKIT cloud behavior.

## Current Boundaries

- Flashing this firmware replaces the original PETKIT firmware.
- Confirm your hardware matches the supported Element Solo model before
  flashing.
- Estimated reserve is calculated from calibrated mechanical portions and recorded
  food changes. Food-drop pulses remain a separate delivery check, not a mass sensor.
- Deep sleep is prepared but not automatically entered yet; scheduling a safe
  sleep policy remains future work.
- Food-drop verification requires the Food Drop Pulses entity to be enabled in
  Home Assistant.

## Sources

- [ESPHome Devices: Petkit Fresh Element Solo Pet Feeder](https://devices.esphome.io/devices/petkit-fresh-element-solo-pet-feeder/)
- [n6ham ESPHome configuration](https://github.com/n6ham/esphome-configs/blob/master/petkit-fresh-element-solo.yaml)
- [Triskae ESPHome configuration gist](https://gist.github.com/Triskae/efab9c34f88badd7c37a06d208b513d7)
- [foxey ESPHome configuration gist](https://gist.github.com/foxey/d9aa8b711ad1a76d3b5271c54302ca09)
- [Reddit: ESPHome on Petkit Solo Feeder](https://www.reddit.com/r/Esphome/comments/v19c7p/esphome_on_petkit_solo_feeder/)
- [Reddit: ESPHome on Petkit Solo Feeder, follow-up](https://www.reddit.com/r/Esphome/comments/108nqwc/esphome_on_petkit_solo_feeder_credits_to/)
- [ESPHome dashboard import documentation](https://esphome.io/components/dashboard_import/)
- [ESPHome factory firmware guidance](https://esphome.io/guides/creators/)
- [Home Assistant blueprint documentation](https://www.home-assistant.io/docs/blueprint/)
- [PETKIT Fresh Element Solo manual](https://instructions.petkit.com/D4_V1.2_20220713.pdf)
