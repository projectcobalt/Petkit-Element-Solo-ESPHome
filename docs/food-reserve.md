# Food tracking

Each feeder tracks its estimated food remaining and consumption in grams,
including feeds while Home Assistant is offline. Home Assistant sends refill
notifications through the feeding blueprint.

## Setup

Configure each feeder separately:

1. Set **Food Capacity** to the weight of food in a full hopper.
2. Weigh the food dispensed over several portions and divide by the portion
   count. Enter the result in **Grams Per Portion**.
3. Fill the hopper fully, then press **Food Full Refill**.
4. Review **Low Food Threshold**. It initially defaults to 20% of capacity.
5. Use one feeding blueprint automation per feeder and select the notification
   targets for its alerts.

Food remaining stays unknown until capacity and calibration are configured and
its first full refill is recorded. Consumption starts counting once calibration
is set, even while food remaining is unknown.

## Refills and counters

- **Food Full Refill** sets food remaining to capacity and resets
  **Consumption Since Full Refill**.
- For a partial top-up, weigh the food added, enter **Food Top Up Amount**, then
  press **Food Record Top Up**. This adds to food remaining without resetting
  either consumption counter.
- **Total Tracked Consumption** accumulates consumption across full refills.
  **Consumption Since Full Refill** covers only the period since the last one.

Refill and configuration changes are rejected while feeding or recovering from
a jam. Top-ups must be positive and cannot take the estimate above capacity.
Changing capacity preserves food remaining and the threshold; capacity cannot
be reduced below either. Calibration changes apply to future portions only.

Every completed mechanical portion counts, including portions completed before
a jam and portions dispensed without food. Rejected feed requests and diagnostic
motor jogs do not count. Feeding and consumption counting continue when the
estimate reaches zero.

## Alerts and sounds

A refill alert is due when known food remaining reaches or falls below the
threshold. While food stays low, reminders are checked at **09:00 in the feeder's
configured timezone**, with at least 24 hours between alerts. An alert after
09:00 therefore skips the next morning's reminder.

If disconnected, the feeder checks for a due alert after reconnecting. Missed
reminders produce one alert rather than a backlog. Timed reminders need a valid
clock. Refilling above the threshold allows a new alert the next time food runs
low; a top-up that leaves food below the threshold does not restart the warning.

A feed that finishes with low food plays a distinct completion sound, including
when that feed crosses the threshold. It works offline and respects **Mute
Sounds**. Jam sounds take priority. Reminder notifications do not play a sound.

Notifications are not confirmed as delivered to your phone. A failed notification
or an unavailable Home Assistant connection can mean an alert is missed.

## Accuracy and resets

Food remaining is estimated from calibrated portions, not measured directly.
Food type, portion variation, spills and unrecorded additions can cause drift.
Food-drop detection is a separate check that food was dispensed.

Tracking is saved on the feeder and normally survives restarts. Abrupt power
loss can leave the estimate inaccurate; erasing device storage or a factory reset
loses tracking. To reset an inaccurate estimate, fill the hopper fully and press
**Food Full Refill**.
