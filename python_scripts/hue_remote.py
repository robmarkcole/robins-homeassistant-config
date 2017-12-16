button_obj = hass.states.get('sensor.living_room_remote_status')
button = button_obj.state
logger.warning("Hello Robin, button preseed was  {}".format(button))

if button == '1':
    hass.services.call('light', 'turn_on', { "entity_id" : 'light.lamp', 'color_name': 'green' })
elif button == '2':
   hass.services.call('light', 'turn_on', { "entity_id" : 'light.lamp', 'color_name': 'red' })
elif button == '3':
   hass.services.call('light', 'turn_on', { "entity_id" : 'light.lamp', 'color_name': 'purple' })
elif button == '4':
   hass.services.call('light', 'turn_on', { "entity_id" : 'light.lamp', 'color_name': 'yellow' })
