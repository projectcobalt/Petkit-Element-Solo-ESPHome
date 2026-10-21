# PETKIT Element Solo for ESPHome

Local firmware and a Home Assistant feeding blueprint for the PETKIT Fresh
Element Solo (D4-2 / P570).

## Features

- Scheduled and manual feeding with configurable portions.
- Jam recovery and food-delivery checks.
- Estimated food remaining, calibrated consumption, full refills and partial top-ups.
- Low-food alerts, daily reminders and sound feedback.
- Child lock and battery/power monitoring.

Food tracking runs on each feeder, including while Home Assistant is offline.
Home Assistant handles meal schedules and notifications. Food remaining is
estimated from calibrated portions, not measured directly.

## Getting started

- [Firmware package](petkit-element-solo.yaml)
- [Home Assistant blueprint](blueprints/automation/element-solo-feeding.yaml)
- [Food calibration and refill controls](docs/food-reserve.md)

## Releases

[Latest release](https://github.com/projectcobalt/Petkit-Element-Solo-ESPHome/releases/latest)
· [Changelog](CHANGELOG.md)

## Credits

Based on community work from [n6ham](https://github.com/n6ham/esphome-configs/blob/master/petkit-fresh-element-solo.yaml),
[Triskae](https://gist.github.com/Triskae/efab9c34f88badd7c37a06d208b513d7)
and [foxey](https://gist.github.com/foxey/d9aa8b711ad1a76d3b5271c54302ca09).

This project is independent of PETKIT.
