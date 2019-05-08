My [home-assistant](https://home-assistant.io/) [configuration](https://home-assistant.io/docs/configuration/) files.

<img src="https://github.com/robmarkcole/robins-homeassistant-config/blob/master/images/front-end.png">

#### HASSIO
I run a hassio on a pi 3. 

#### Hue sensors
I have Philips Hue remotes and motion sensors. I wrote a custom component to integrate them [here](https://github.com/robmarkcole/Hue-sensors-HASS).

#### Water leak detector
My leak detector is a DIY sensor using micropython, with a writeup on [Hackster](https://www.hackster.io/robin-cole/micropython-leak-detector-with-adafruit-and-home-assistant-a2fa9e).

#### BME680 Temperature, humidity and air quality sensors
CURRENTLY NOT USING: I branched a [Pimoroni library](https://github.com/pimoroni/bme680) for the BME680 to publish data over MQTT, repo [here](https://github.com/robmarkcole/bme680-mqtt-micropython).

#### Automation to boil my kettle in the morning
I own an [Appkettle](https://www.myappkettle.com/) which is integrated with HA via IFTTT. Write up on [Hackster](https://www.hackster.io/robin-cole/boil-my-kettle-when-i-get-out-of-bed-in-the-morning-10e7de).

#### Late train notification via Hue lamp
If my train is late, a Hue light turns red. On [Hackster](https://www.hackster.io/robin-cole/traffic-light-alerts-for-my-morning-train-350a27).

#### Elgato HomeKit sensors
My [Elgato door sensor](https://www.elgato.com/en/eve/eve-door-window) cannot be integrated directly into HA since it is HomeKit only. To get around this I use the Homebridge addon for Hassio. See [this thread](https://community.home-assistant.io/t/triggar-ha-from-homekit-devices/3253/5). The same trick works for my [Fibaro leak sensor](https://www.fibaro.com/en/products/flood-sensor/).

#### MacBook sensor
I have a sensor which is ON when I am using my MacBook. I did this using Hammerspoon as [described here](https://github.com/robmarkcole/HASS-hammerspoon).

#### RF doorbell
I integrate an RF doorbell using an Arduino which relays signals over the serial port, as [described here](https://github.com/robmarkcole/RF-doorbell-serial).

#### Python scripts
I am a big fan of using python_scripts over long YAML automations. I have a [dedicated repo here](https://github.com/robmarkcole/python-scripts-for-home-assistant).

#### Google Cloud SQL recorder
I use a Google cloud SQL database as a recorder, as [described here](https://github.com/robmarkcole/HASS-Google-Cloud-SQL).

#### Bayesian 'in bed' sensor
My own bayesian 'in bed bayesian sensor' is working nicely after a lot of experimentation. I found that the 'sun below horizon' input wasn't particularly useful, since in the UK at this time of year the sun is setting before 5pm.! Instead I'm using a template sensor which is ON at 'late night'.

```yaml
- platform: template
  sensors:
    late_night_sensor:
      value_template: >-
          {{ strptime("22:00", "%H%M")  < now().strftime("%H:%M")
             or now().strftime("%H:%M") < strptime("07:00", "%H%M") }}
```
As a couple of others have done I also have a sensor to detect when there has been no motion in the house for 5 minutes. I implemented that using an input_select and an automation:

```yaml
- id: '1513346519354'
  alias: House_idle
  trigger:
  - entity_id: binary_sensor.motion_at_home
    for:
      minutes: 5
    from: 'on'
    platform: state
    to: 'off'
  action:
  - data:
      entity_id: input_boolean.house_idle
    service: input_boolean.turn_on
```

Finally the bayesian sensor is:
```yaml
- platform: 'bayesian'
  name: 'in_bed_bayesian'
  prior: 0.25
  observations:
    - entity_id: 'input_boolean.house_idle'
      prob_given_true: 0.6
      platform: 'state'
      to_state: 'on'
    - entity_id: 'binary_sensor.late_night_sensor'
      prob_given_true: 0.8
      platform: 'state'
      to_state: 'on'
    - entity_id: 'binary_sensor.motion_at_home'
      prob_given_true: 0.1
      platform: 'state'
      to_state: 'on'
    - entity_id: 'switch.macbook_power'
      prob_given_true: 0.1
      platform: 'state'
      to_state: 'on'
    - entity_id: 'switch.tv'
      prob_given_true: 0.1
      platform: 'state'
      to_state: 'on'
```

I am using the [history statistics](https://home-assistant.io/components/sensor.history_stats/) component and a template sensor to display the number of hours I spent in bed last night.
```yaml
- platform: history_stats
  name: Time in bed
  entity_id: binary_sensor.in_bed_bayesian
  state: 'on'
  type: time
  end: '{{ now() }}'
  duration:
    hours: 24
```

And the template sensor:
```yaml
- platform: template
  sensors:
    time_in_bed_template:
      friendly_name: 'Time in bed'
      value_template: '{{states.sensor.time_in_bed.attributes.value}}'
```
Lastly, I wrote a notebook discussing the ideas behind the bayesian sensor, and many thanks to @jlmcgehee21 for all his edits:
http://nbviewer.jupyter.org/github/robmarkcole/HASS-data-science/blob/master/Bayesian%20sensor%20tutorial.ipynb

## Hassio Add-ons
Try to limit your addons, as too many will make your system unstable.
1. IDE: https://github.com/hassio-addons/addon-ide
2. SSH & Web Terminal:  https://github.com/hassio-addons/addon-ssh/blob/v3.2.0/README.md
3. MQTT Server & Web client: https://github.com/hassio-addons/addon-mqtt/blob/master/README.md
4. Motion camera detection: https://github.com/HerrHofrat/hassio-addons
5. Glances: https://github.com/hassio-addons/addon-glances
6. Jupyterlab Lite: https://github.com/hassio-addons/addon-jupyterlab-lite
7. Log Viewer: https://github.com/hassio-addons/addon-log-viewer
