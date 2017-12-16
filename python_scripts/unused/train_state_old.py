entity_id = 'sensor.next_train_to_wim'
attributes = hass.states.get(entity_id).attributes

my_early_train_current_status = hass.states.get('sensor.my_early_train').state

scheduled = False   # Check if train scheduled

for train in attributes['next_trains']:
    if train['scheduled'] == '07:15':
        scheduled = True
        if train['status'] != my_early_train_current_status:
            hass.states.set('sensor.my_early_train', train['status'])

if not scheduled:
    hass.states.set('sensor.my_early_train', 'No data')  # check no data
