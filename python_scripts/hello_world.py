name = data.get('name', 'world')
logger.info("Hello Robin {}".format(name))
hass.bus.fire(name, { "wow": "from a Python script!" })


state = hass.states.get('sensor.next_train_status')
train_status = state.state

if train_status == 'ON TIME':
    hass.services.call('light', 'turn_on', { "entity_id" : 'light.lamp', 'color_name': 'green' })
else:
   hass.services.call('light', 'turn_on', { "entity_id" : 'light.lamp', 'color_name': 'red' })
