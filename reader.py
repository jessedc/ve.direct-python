#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import serial
from vedirect import Vedirect
import paho.mqtt.client as mqtt


mqttc = mqtt.Client('319a-victron-mppt')
mqttc.username_pw_set('iot-user', 'avrdragon')

base_topic = 'victron-mppt/'
# last_victron_data = None
victron_key_map = {
    'LOAD': 'now/battery-state',
    'H19': 'total/yield',
    'VPV': 'now/pv-voltage',
    'ERR': 'now/error',
    'FW': 'system/firmware',
    'I': 'now/battery-current',
    'H21': 'now/max-power',
    'IL': 'now/load-current',
    'PID': 'system/pid',
    'H20': 'now/yield',
    'H23': 'yesterday/max-power',
    'MPPT': 'now/mppt-state',
    'HSDS': 'system/day-seq',
    'SER#': 'system/serial-no',
    'V': 'now/battery-voltage',
    'CS': 'now/state',
    'H22': 'yesterday/yield',
    'PPV': 'now/pv-power'
}

victron_state = {
    '0': 'Off',
    '2': 'Fault',
    '3': 'Bulk',
    '4': 'Absorption',
    '5': 'Float'
}


def on_victron_data_callback(data):
    for key, value in data.iteritems():
        if key == 'CS':
            value = victron_state[value]

        key = victron_key_map[key]
        mqttc.publish(base_topic + key, value)


mqttc.connect('10.0.1.212')
mqttc.loop_start()

ve = Vedirect('/dev/ttyAMA0', 1)
ve.read_data_callback(on_victron_data_callback)


