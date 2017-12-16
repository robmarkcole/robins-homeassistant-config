entity_id = 'sensor.my_early_train'
status = hass.states.get(entity_id).state

time = hass.states.get('sensor.time').state

#hass.services.call('notify', 'ios_robins_iphone',
#    {'title':'Script', 'message':'my_7_45_train.py ran at {}'.format(time)})

if status not in ['No data', 'EARLY', 'NO REPORT']:
    if status == 'ON TIME':
        hass.services.call('light', 'turn_on', { "entity_id" : 'light.lamp', 'color_name': 'green' })
    elif status == 'LATE':
        hass.services.call('light', 'turn_on', { "entity_id" : 'light.lamp', 'color_name': 'orange' })
    elif status == 'CANCELLED':
        hass.services.call('light', 'turn_on', { "entity_id" : 'light.lamp', 'color_name': 'red' })
    hass.services.call('notify', 'robins_and_marias_iphones',
        {'title':'7:15 train update', 'message':'Train status is {}'.format(status)})
