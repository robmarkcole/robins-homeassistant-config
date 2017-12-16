tempEntities = ["sensor.bedroom_temperature",
               "sensor.blink_blink_camera_percy_temperature",
               "sensor.hall_temperature",
               "sensor.living_room_temperature"]

sensorsTotal = len(tempEntities)
tempsCounted = 0
tempsTotal = 0

# look up each entity_id
for entity_id in tempEntities:
  # copy it's state
  state = hass.states.get(entity_id)

  # If not None, add up and increase counter
  if state.state is not 'unknown':
     tempsCounted = tempsCounted + 1
     tempsTotal = tempsTotal + float(state.state)

# Get average
averageTemp = tempsTotal / tempsCounted
averageTemp = round(averageTemp, 1)
# logger.warning("Ave indoor temp of : {}".format(averageTemp))

hass.states.set('sensor.average_indoor_temp', averageTemp, {
    'unit_of_measurement': '°C',
    'friendly_name': 'Indoor Temp',
    'icon': 'mdi:thermometer',
    'temps_counted': tempsCounted,
    'temps_total': sensorsTotal
})
