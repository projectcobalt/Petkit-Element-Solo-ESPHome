# Food reserve tracking

Each feeder owns its reserve estimate, consumption totals, low-food detection and
reminder timing. The implementation uses native ESPHome globals, scripts, time,
event and template entities. The existing Home Assistant blueprint forwards refill
events to its notification targets and continues scheduling/supervising meals.

## Configure each feeder

1. Set **Food Capacity** to the weighed grams at your normal full-hopper level.
2. Weigh several normal portions, subtract the container weight, and divide by
   the portion count. Set **Grams Per Portion** separately for each feeder.
3. Fill the hopper to the configured capacity, then press **Food Full Refill**.
   Installation starts with unknown reserve until the first full refill.
4. Review **Low Food Threshold**, initially 20% of the first configured capacity.
   Later capacity changes preserve the threshold in grams.
5. Keep one blueprint instance per feeder, select its device, meal schedules and
   existing error-notification targets. No Home Assistant timing helper is needed.

Capacity and calibration are required before reserve can be established.
Consumption starts once calibration is valid even if reserve remains unknown.
The blueprint requires Home Assistant 2026.7+ for its native `event.received`
trigger; production was inspected read-only and runs 2026.10.0.

## Refills and consumption

- **Full refill** sets reserve to capacity and resets consumption since full refill.
- **Top-up amount / Record top up** adds weighed grams without resetting totals.

Changes during feeding/jam recovery and invalid or over-capacity amounts are
rejected. Capacity cannot be lowered below reserve or threshold. Calibration
changes affect future feeds only; previous consumption is never recalculated.

Every completed mechanical portion counts, including dry portions and portions
before a jam. Scheduled, manual and offline feeds use the same accounting path.
Rejected requests and diagnostic motor jogs do not count. Reserve floors at zero;
feeding and consumption totals continue.

## Device-owned warnings and sound

The feeder evaluates low food after portions and food edits. A known reserve at
or below threshold is low. The first warning emits `food_refill_needed` on the
separate **Food Reserve Event** entity. The blueprint's native event trigger
scopes this to the selected feeder and forwards it to existing error targets.
This event cannot interfere with the separate feed-completion event waiter.
Missing numeric telemetry does not suppress a refill notification.

The device uses its RTC-backed clock and configured timezone (Brisbane by default)
to check reminders at 09:00. It persists whether the current low condition was
already warned and the last event's epoch. A reminder requires at least 24 hours
since that event. For example, an initial warning at 10:00 means the next day's
09:00 check is too soon; the following eligible 09:00 check can remind.

Checks while disconnected leave the warning due. After an entity-state client
connects and remains subscribed for ten seconds, the device reassesses initial or
overdue warnings. This also covers device/HA restarts. Repeated connections do not
reemit a recent warning. Refilling above threshold rearms a new initial warning;
a top-up that leaves reserve low does not. Multiple missed days produce one due
warning, rather than replaying a backlog.

Without valid clock time, an initial warning can still emit once. Timed reminders
wait for valid time. If the first warning had no timestamp, the device anchors
its reminder clock when valid time returns, without issuing a duplicate. Existing
SNTP synchronization maintains the hardware RTC when the network is available.

When a feed completes at/below threshold, **sound_feed_low_food** replaces the
normal completion tune. It also covers crossing the threshold during that feed,
works offline and respects **Mute Sounds**. Unknown reserve uses the normal tune.
Jam/error sounds retain priority. Merely reaching 09:00 does not play a sound.
The tune can be overridden through the standard ESPHome RTTTL substitution.

## Limits

The recorded time means **event emitted**, not successful phone delivery. A
failed/disabled notification destination can miss that event until the next due
check. There is no acknowledgement protocol. Native API state subscribers are
normally HA, but another subscribing client (including the ESPHome log viewer)
can receive/consume a warning while HA is offline. External delivery and saves
are best effort; this is not an event queue.

Device globals save after portions, food edits and warning-state changes.
Separate scalar saves and physical dispensing are not transactional. Abrupt power
loss can leave discrepancies; fill to capacity and record a full refill after uncertainty.
Flash erasure/factory reset loses tracking. The estimate can drift with food,
mechanical variation, spills or unrecorded additions. Optical food-drop warnings
remain a separate check of actual delivery.

## Validation and rollout

Local firmware builds with ESPHome 2026.9.1+. Run `esphome config` and
`esphome compile` on the package and intended adopted configurations.

With a supported Home Assistant runtime, run:

```powershell
python tests/validate_ha_schema.py
```

An isolated HA package directory may be supplied. `--allow-older-ha` permits
partial validation on the existing local 2024.10 test runtime: it checks selectors,
actions and older trigger schemas and executes the real refill action branch
against a fake notification destination. It explicitly skips the modern
`event.received` runtime schema; that trigger's shape was checked against official
2026.10 documentation/source. Production HA 2026.10.0 subsequently accepted the
exact new trigger and full instantiated blueprint triggers/actions for both
feeders via ha-mcp and the non-saving `validate_config` WebSocket command.
Neither the validation nor local checks exercise event delivery or hardware.
Before deployment, retain the current adopted YAML, firmware, blueprint and
inputs, and record any existing tracking values. Update the matching blueprint
before firmware so its refill listener is ready. Preserve schedules and targets,
and keep one instance per feeder. The removed local-only `refill_alert_last_sent`
input is no longer used; remove it from any experimental automation inputs before
reimport. Production never received that intermediate helper-based version.
Verify accounting, RTC time, reboot/reconnect behavior, sound/mute and actual
notification delivery during a controlled device check. After rollbacks or uncertain power loss, refill fully and record the full refill.

References: [ESPHome event entities](https://esphome.io/components/event/),
[ESPHome time](https://esphome.io/components/time/),
[API subscription conditions](https://esphome.io/components/api/#api-connected-condition),
[HA event received trigger](https://www.home-assistant.io/triggers/event.received/).

On 19 October 2026, the separate correction amount and apply button were removed.
The supported food adjustments are Full Refill and Top Up. To reset an estimate
that has drifted, fill the hopper fully and record Full Refill. Capacity remains
a configuration setting and does not directly change the reserve estimate.
