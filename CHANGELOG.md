# Changelog

## v2.0.0 - 22 October 2026

- Added estimated food remaining in grams, with capacity and portion calibration
  configured separately for each feeder.
- Added total tracked consumption and consumption since the last full refill.
- Added full-refill and partial top-up controls.
- Added food tracking that continues offline and survives normal restarts.
- Added low-food notifications and daily reminders through the feeding blueprint.
- Added a distinct low-food completion sound that respects Mute Sounds.
- Requires ESPHome 2026.9.1 or later and Home Assistant 2026.7 or later.

## v1.2.0

- Added a Child Lock switch that prevents the physical side button from starting
  a manual feed while leaving Home Assistant and API feed requests available.

## v1.1.0

- Improved portion counting by filtering repeated motor pulses.
- Added Food State and Battery Pack Level entities.
- Made status LED behavior consistent and added configurable sound feedback.
- Fixed feed confirmation in the Home Assistant blueprint for repeated feeds.
- Improved compatibility when looking up the feeder's state in Home Assistant.

## v1.0.0

- Initial public ESPHome package for the PETKIT Fresh Element Solo.
- Added Home Assistant blueprint for scheduled feeding, supervision, and
  notifications.
