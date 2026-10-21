# Changelog

## v2.0.0 - 22 October 2026

- Removed Food Reserve Correction Amount and Food Apply Reserve Correction.
- Retained Full Refill and Top Up, existing counters/calibration, capacity rules,
  low-food reminders and sounds.

## 1.3.0-dev

- Added independent device-owned food reserve estimates in grams, per-feeder
  calibration, and total/since-full-refill consumption.
- Added validated full-refill, top-up, and correction controls; unknown reserve
  remains distinct from known zero and estimates never block feeding.
- Save native ESPHome scalar globals after completed portions and food changes
  for offline/restart accounting; multi-value saves are not atomic.
- Moved low-food checks, 09:00 reminders, reconnect assessment and persistent
  warning timestamps onto the feeder, using its RTC-backed clock.
- Added a separate Food Reserve Event (`food_refill_needed`); the consolidated
  blueprint forwards it to existing error-notification targets. No HA time helper.
- Added a distinct mute-aware low-food feed-completion tune, including feeds
  crossing the threshold. Jam/error sounds retain priority.
- Blueprint now requires HA 2026.7+ for native `event.received` targeting the feeder.
- Retained the production model selector and meal schedules/notification targets.
- Removed the custom accounting header and notification claim/lease protocol.
- Local checks and limitations are recorded in the implementation report.


## v1.2.0

- Added a Child Lock switch that prevents the physical side button from starting
  a manual feed while leaving Home Assistant and API feed requests available.

## v1.1.0

- Added motor pulse lockout for more reliable portion counting.
- Added Food State and Battery Pack Level entities.
- Centralized status LED behavior and RTTTL sound substitutions.
- Added dormant deep-sleep wake plumbing on the manual feed button.
- Fixed the Home Assistant blueprint feed confirmation wait so repeated feed
  completions are handled as fresh events.
- Made the blueprint Feeder State lookup tolerant of `sensor` and `text_sensor`
  entity domains.

## v1.0.0

- Initial public ESPHome package for the PETKIT Fresh Element Solo.
- Added Home Assistant blueprint for scheduled feeding, supervision, and
  notifications.
