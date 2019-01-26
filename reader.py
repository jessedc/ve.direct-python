#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import serial
from vedirect import Vedirect
import paho.mqtt.client as mqtt

mqttc = mqtt.Client('319a-victron-mppt')
mqttc.username_pw_set('iot-user', 'avrdragon')
broker_ip = '192.168.1.15'

base_topic = 'victron/mppt/'

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

mppt_state = {
    '0': 'Off',
    '1': 'Limited',
    '2': 'Active'
}

victron_error = {
    '0': 'No error [error 0]',
    '2': 'Battery voltage too high [error 2]',
    '17': 'Charger temperature too high [error 17]',
    '18': 'Charger over current [error 18]',
    '19': 'Charger current reversed [error 19]',
    '20': 'Bulk time limit exceeded [error 20]',
    '21': 'Current sensor issue [error 21]',
    '26': 'Terminals overheated [error 26]',
    '33': 'Input voltage too high (solar panel) [error 33]',
    '34': 'Input current too high (solar panel) [error 34]',
    '38': 'Input shutdown (excessive battery voltage) [error 38]',
    '116': 'Factory calibration data lost [error 116]',
    '117': 'Invalid/incompatible firmware [error 117]',
    '119': 'User settings invalid [error 119]'
}

# Local variable to store previous frame
# previous_victron_frame = {}


def on_victron_data_callback(data):
    # global previous_victron_frame

    for key, value in data.iteritems():
        # NB: To filter values, do something like this:
        # if previous_victron_frame.get(key, None) == value:
        #     continue
        # else:
        #     previous_victron_frame[key] = value

        if key == 'CS':
            value = victron_state[value]
        elif key == 'MPPT':
            value = mppt_state[value]
        elif key == 'ERR':
            value = victron_error[value]

        key = base_topic + victron_key_map[key]
        mqttc.publish(key, value)


mqttc.connect(broker_ip)
mqttc.loop_start()

ve = Vedirect('/dev/ttyAMA0', 1)
ve.read_data_callback(on_victron_data_callback)
