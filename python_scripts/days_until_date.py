"""
Script to create a sensor displaying the number of days until some event.
Automate to update every day.
"""

EVENT = 'renew_letsencrypt'
YEAR = 2018
MONTH = 2
DAY = 8

day_of_interest = datetime.datetime(YEAR, MONTH, DAY)
now = datetime.datetime.now()
diff = day_of_interest - now

hass.states.set('sensor.' + EVENT, diff.days,{
    'unit_of_measurement': 'days',
    'friendly_name': 'Days until renew LetsEncrypt',
    'icon': 'mdi:calendar'
})
