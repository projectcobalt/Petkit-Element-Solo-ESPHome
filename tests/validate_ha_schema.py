"""Validate blueprint schemas and execute its refill notification branch locally.

python tests/validate_ha_schema.py [isolated-package-directory] [--allow-older-ha]
Older HA can check actions/legacy triggers, but cannot validate event.received.
No server, feeder connection or real notification is started.
"""
import asyncio
import copy
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
args = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
if args:
    sys.path.insert(0, str(Path(args[0]).resolve()))

from homeassistant.core import HomeAssistant, Context
from homeassistant import loader
from homeassistant.const import __version__
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import selector
from homeassistant.helpers.script import Script
from homeassistant.helpers.template import Template
from homeassistant.helpers.trigger import async_validate_trigger_config
from homeassistant.util import yaml


async def validate(hass):
    loader.async_setup(hass)
    document = yaml.load_yaml(str(ROOT / 'blueprints/automation/element-solo-feeding.yaml'))
    inputs = {}
    for section in document['blueprint']['input'].values():
        for name, definition in section['input'].items():
            selector.validate_selector(definition['selector'])
            if 'default' in definition:
                inputs[name] = definition['default']
    inputs.update(feeder_device='0123456789abcdef0123456789abcdef', schedule_triggers=[
        {'trigger': 'sun', 'event': 'sunrise'}, {'trigger': 'sun', 'event': 'sunset'}])
    old_runtime = tuple(int(part) for part in __version__.split('.')[:2]) < (2026, 7)
    if old_runtime and '--allow-older-ha' not in sys.argv:
        raise RuntimeError('This blueprint needs HA 2026.7+. Use --allow-older-ha for partial validation.')
    for native in (False, True):
        selected = dict(inputs)
        if native:
            selected.update(native_feed_action='esphome.validation_feed')
        config = yaml.substitute(copy.deepcopy(document), selected)
        cv.SCRIPT_SCHEMA(config['actions'])
        triggers = cv.TRIGGER_SCHEMA(config['triggers'])
        # The local 2024 test runtime predates purpose-specific triggers. Never
        # imply that validating the remaining triggers validates the new trigger.
        if old_runtime:
            triggers = [item for item in triggers if item['platform'] != 'event.received']
        await async_validate_trigger_config(hass, triggers)
        cv.SCRIPT_VARIABLES_SCHEMA(config['variables'])
        cv.SCRIPT_VARIABLES_SCHEMA(config['trigger_variables'])
        print(('Native feed' if native else 'Default inputs') + ': selectors/actions/available trigger schemas passed')
    if old_runtime:
        print('PARTIAL: event.received runtime schema requires HA 2026.7+; shape checked against official 2026.10 docs/source.')

    # Execute the real refill branch through HA's Script engine. Mock only the
    # external notification destination; absent telemetry must not lose an event.
    branch = next(branch for branch in config['actions'][1]['choose']
        if branch['conditions'][0].get('id') == 'food_refill_needed')
    sent = []
    async def notify(call):
        sent.append(call.data)
    hass.services.async_register('notify', 'send_message', notify)
    script = Script(hass, cv.SCRIPT_SCHEMA(branch['sequence']), 'Refill validation', 'petkit')
    variables = dict(feeder_name='Test feeder', error_notify_targets=['notify.validation'],
        estimated_food_remaining='sensor.validation_remaining', low_food_threshold='number.validation_threshold')
    await script.async_run(variables, context=Context())
    assert len(sent) == 1 and 'requests a food refill' in sent[-1]['message']
    assert 'unknown' not in sent[-1]['message']
    hass.states.async_set('sensor.validation_remaining', '100')
    hass.states.async_set('number.validation_threshold', '200')
    await script.async_run(variables, context=Context())
    assert len(sent) == 2 and '100.0 g' in sent[-1]['message'] and '200.0 g' in sent[-1]['message']
    await script.async_run(dict(variables, error_notify_targets=[]), context=Context())
    assert len(sent) == 2, 'An empty destination should not attempt a notification'
    gate = Template(str(config['actions'][0]['value_template']), hass)
    assert gate.async_render(dict(native_feed_action='', this={'attributes': {'current': 1}},
        trigger={'id': 'food_refill_needed'})) is True
    print('HA Script: refill forwards with/without telemetry, empty targets skip; meal wait permits alert')


async def main():
    hass = HomeAssistant(str(ROOT / '.build/ha-validation'))
    try:
        await validate(hass)
    finally:
        hass.import_executor.shutdown()


if __name__ == '__main__':
    asyncio.run(main())
