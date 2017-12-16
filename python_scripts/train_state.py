"""
Script to receive alerts for train of interest (TOI).
"""
SCHEDULED = False

# Set config
MAIN_ENTITY_ID = 'sensor.next_train_to_wim'
TOI_ENTITY_ID = 'sensor.morning_train'
TOI_TIME = '07:15'

# Set notification details
MSG_TITLE = "Train Status Update"
NOTIFY_ID = 'robins_and_marias_iphones'


if hass.states.get(MAIN_ENTITY_ID).state == "No departures":
    logger.warn('No Departures')
else:
    attributes = hass.states.get(MAIN_ENTITY_ID).attributes
    try:
        for train in attributes['next_trains']:
            if train['scheduled'] == TOI_TIME:
                SCHEDULED = True
                train_status = train['status']

                if train_status != hass.states.get(TOI_ENTITY_ID).state:
                    hass.states.set(TOI_ENTITY_ID, train_status)

                    if train_status == 'LATE':
                        hass.services.call('notify', NOTIFY_ID, {
                            "title": MSG_TITLE,
                            "message": "The {} will be late and its ETA is"
                            .format(TOI_TIME) + train['estimated']})

                        hass.services.call('light', 'turn_on', {
                            "entity_id": 'light.lamp',
                            'color_name': 'orange'})

                    elif train_status == 'CANCELLED':
                        hass.services.call('notify', NOTIFY_ID, {
                            "title": MSG_TITLE,
                            "message": "The {} has been cancelled."
                            .format(TOI_TIME)})

                        hass.services.call('light', 'turn_on', {
                            "entity_id": 'light.lamp',
                            'color_name': 'red'})
                break
    except:
        logger.warn('Error in train_state.py')

if not SCHEDULED:
    hass.states.set(TOI_ENTITY_ID, 'No data')  # check no data
